RECOMMENDATIONS = {
    "forward_head": [
        "Chin tucks",
        "Upper trapezius stretch",
        "Levator scapulae stretch",
        "Thoracic extension over chair",
    ],
    "rounded_shoulders": [
        "Doorway chest stretch",
        "Wall angels",
        "Band pull-aparts",
        "Scapular retractions",
    ],
    "uneven_shoulders": [
        "Gentle neck side stretch",
        "Scapular retractions",
        "Shoulder blade squeezes",
        "Single-arm doorway stretch",
    ],
    "uneven_hips": [
        "Hip flexor stretch",
        "Glute bridges",
        "Side planks",
        "Clamshells",
    ],
}


def get_recommendations(recommendation_key):
    """
    Return exercise suggestions for a posture finding.
    """

    return RECOMMENDATIONS.get(
        recommendation_key,
        ["General mobility work", "Light stretching", "Posture awareness exercises"],
    )