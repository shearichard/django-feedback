from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from feedback.forms import AnonymousFeedbackForm, FeedbackForm


def leave_feedback(request, template_name='feedback/feedback_form.html'):
    if request.method == "GET":
        nexturl = request.GET.get('next')
    else:
        nexturl = request.POST.get('next')

    if request.user.is_authenticated():
        form = FeedbackForm(request.POST or None)
    else:
        form = AnonymousFeedbackForm(request.POST or None)
    if form.is_valid():
        feedback = form.save(commit=False)
        if request.user.is_anonymous():
            feedback.user = None
        else:
            feedback.user = request.user
        feedback.save()
        messages.add_message(request, messages.SUCCESS,
                             'Your feedback was submitted.')
        return HttpResponseRedirect(nexturl)

    return render_to_response(
                                template_name, 
                                {
                                'feedback_form': form,
                                'next': nexturl
                                },
                                context_instance=RequestContext(request))
