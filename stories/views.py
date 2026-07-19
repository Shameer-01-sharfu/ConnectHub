from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone

from .forms import StoryForm

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import (
    Story,
    StorySeen,
    Highlight,
    HighlightStory,
    StoryReaction,
)


@login_required
def upload_story(request):

    if request.method == "POST":

        form = StoryForm(request.POST, request.FILES)

        if form.is_valid():

            story = form.save(commit=False)
            story.user = request.user
            story.save()

            return redirect("home")

    else:

        form = StoryForm()

    return render(
        request,
        "stories/upload_story.html",
        {
            "form": form
        }
    )


@login_required
def user_stories(request, user_id):

    story_user = get_object_or_404(User, id=user_id)

    stories = Story.objects.filter(
        user=story_user,
        expires_at__gt=timezone.now()
    ).order_by("created_at")

    if not stories.exists():
        return redirect("home")

    story_index = int(request.GET.get("index", 0))

    if story_index >= stories.count():
        return redirect("home")

    current_story = stories[story_index]

    # Save Story Seen
    if request.user != story_user:
        StorySeen.objects.get_or_create(
            story=current_story,
            user=request.user
        )

    # Seen Details
    seen_users = StorySeen.objects.filter(
        story=current_story
    ).select_related("user")

    seen_count = seen_users.count()

    # Next Story URL
    if story_index + 1 < stories.count():
        next_url = f"/stories/user/{user_id}/?index={story_index + 1}"
    else:
        next_url = "/"

    return render(
        request,
        "stories/story_view.html",
        {
            "story": current_story,
            "story_user": story_user,
            "next_url": next_url,
            "current_index": story_index + 1,
            "total": stories.count(),
            "seen_users": seen_users,
            "seen_count": seen_count,
        },
    )

@login_required
def react_story(request, story_id, emoji):

    story = get_object_or_404(
        Story,
        id=story_id
    )

    StoryReaction.objects.update_or_create(
        story=story,
        user=request.user,
        defaults={
            "emoji": emoji
        }
    )

    return redirect(
        "user_stories",
        user_id=story.user.id
    )

@login_required
def create_highlight(request):

    if request.method == "POST":

        title = request.POST.get("title")
        cover = request.FILES.get("cover")

        highlight = Highlight.objects.create(
            user=request.user,
            title=title,
            cover=cover
        )

        # Latest Story
        latest_story = Story.objects.filter(
            user=request.user
        ).order_by("-created_at").first()

        if latest_story:

            HighlightStory.objects.create(
                highlight=highlight,
                story=latest_story
            )

        messages.success(
            request,
            "Highlight Created Successfully."
        )

        return redirect("profile")

    return render(
        request,
        "stories/create_highlight.html"
    )


@login_required
def add_story_to_highlight(request, story_id):

    story = get_object_or_404(
        Story,
        id=story_id,
        user=request.user
    )

    if request.method == "POST":

        highlight = get_object_or_404(
            Highlight,
            id=request.POST.get("highlight"),
            user=request.user
        )

        HighlightStory.objects.create(
            highlight=highlight,
            story=story
        )

        messages.success(
            request,
            "Story Added to Highlight."
        )

        return redirect("profile")

    highlights = Highlight.objects.filter(
        user=request.user
    )

    return render(
        request,
        "stories/add_story_highlight.html",
        {
            "story": story,
            "highlights": highlights,
        }
    )

@login_required
def view_highlight(request, highlight_id):

    highlight = get_object_or_404(
        Highlight,
        id=highlight_id
    )

    stories = Story.objects.filter(
    highlightstory__highlight=highlight
).order_by("created_at")
    return render(
        request,
        "stories/view_highlight.html",
        {
            "highlight": highlight,
            "stories": stories,
        },
    )

@login_required
def react_story(request, story_id, emoji):

    story = get_object_or_404(
        Story,
        id=story_id
    )

    StoryReaction.objects.update_or_create(
        story=story,
        user=request.user,
        defaults={
            "emoji": emoji
        }
    )

    return redirect(
        f"/stories/user/{story.user.id}/"
    )