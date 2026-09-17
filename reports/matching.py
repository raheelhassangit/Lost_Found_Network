MATCH_THRESHOLD = 40


def calculate_score(a, b):
    score = 0

    if a.category_id and a.category_id == b.category_id:
        score += 30

    loc_a, loc_b = a.location.strip().lower(), b.location.strip().lower()
    if loc_a and loc_b:
        if loc_a == loc_b:
            score += 25
        elif loc_a in loc_b or loc_b in loc_a:
            score += 15

    days_apart = abs((a.date - b.date).days)
    if days_apart <= 1:
        score += 20
    elif days_apart <= 3:
        score += 15
    elif days_apart <= 7:
        score += 10
    elif days_apart <= 14:
        score += 5

    color_a, color_b = a.color.strip().lower(), b.color.strip().lower()
    if color_a and color_b and color_a == color_b:
        score += 15

    words_a = set(a.description.lower().split())
    words_b = set(b.description.lower().split())
    if words_a and words_b:
        overlap = len(words_a & words_b) / len(words_a | words_b)
        score += round(overlap * 10)

    return min(score, 100)


def generate_matches(report):
    from .models import Report, Match

    opposite_type = Report.ReportType.FOUND if report.report_type == Report.ReportType.LOST else Report.ReportType.LOST
    candidates = Report.objects.filter(
        report_type=opposite_type,
        status__in=[Report.Status.OPEN, Report.Status.PROCESSING],
    ).exclude(user=report.user)

    matched_any = False
    for candidate in candidates:
        score = calculate_score(report, candidate)
        if score >= MATCH_THRESHOLD:
            matched_any = True
            Match.objects.get_or_create(
                primary_report=report, matched_report=candidate,
                defaults={"score": score},
            )
            Match.objects.get_or_create(
                primary_report=candidate, matched_report=report,
                defaults={"score": score},
            )

    if matched_any and report.status == Report.Status.OPEN:
        report.status = Report.Status.PROCESSING
        report.save(update_fields=["status"])