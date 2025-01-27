from django.shortcuts import render, get_object_or_404
from .models import UserJourney, JourneyStage, JourneyAction, UserFeedback

def journey_map(request, journey_id):
    # Fetch the journey and its related stages, actions, and feedback in a single query
    journey = get_object_or_404(
        UserJourney.objects.prefetch_related(
            'stages__actions__feedbacks'
        ).select_related(),  # Add any other related fields if needed
        id=journey_id
    )

    # Prepare data for the template
    journey_data = {
        'journey': journey,
        'stages': []
    }

    # Use prefetched data to avoid additional queries
    for stage in journey.stages.all().order_by('order'):
        stage_data = {
            'stage': stage,
            'actions': []
        }

        for action in stage.actions.all().order_by('order'):
            action_data = {
                'action': action,
                'feedbacks': action.feedbacks.all()
            }
            stage_data['actions'].append(action_data)

        journey_data['stages'].append(stage_data)

    return render(request, 'journey_map.html', {'journey_data': journey_data})