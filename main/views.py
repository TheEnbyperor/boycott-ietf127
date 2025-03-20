from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse
from django.conf import settings
from . import forms, models

def index(request):
    unable_to_travel_count = models.Signature.objects.filter(
        situation="unable",
        validated=True
    ).count()
    unwilling_to_travel_count = models.Signature.objects.filter(
        situation="unwilling",
        validated=True
    ).count()
    supporters_count = models.Signature.objects.filter(
        situation="support",
        validated=True
    ).count()

    unable_to_travel_public = models.Signature.objects.filter(
        situation="unable",
        validated=True,
        public=True
    )
    unwilling_to_travel_public = models.Signature.objects.filter(
        situation="unwilling",
        validated=True,
        public=True
    )
    supporters_public = models.Signature.objects.filter(
        situation="support",
        validated=True,
        public=True
    )

    if request.method == "POST":
        form = forms.SignatureForm(request.POST)

        if form.is_valid():
            form.save()

            verify_link = settings.EXTERNAL_URL_BASE + reverse("verify_signature", kwargs={
                "token": form.instance.token,
            })
            text_content = render_to_string(
                "email/verify.txt",
                context={
                    "verify_link": verify_link
                },
            )
            html_content = render_to_string(
                "email/verify.html",
                context={
                    "verify_link": verify_link,
                },
            )
            msg = EmailMultiAlternatives(
                "Verify your signature",
                text_content,
                None,
                [form.cleaned_data["email"]]
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            messages.success(request, "We've sent you an email to verify your signature.")
            form = forms.SignatureForm()
    else:
        form = forms.SignatureForm()

    return render(request, "main/index.html", {
        "form": form,
        "counts": {
            "unable_to_travel": unable_to_travel_count,
            "unwilling_to_travel": unwilling_to_travel_count,
            "supporters": supporters_count,
        },
        "public_signatures": {
            "unable_to_travel": unable_to_travel_public,
            "unwilling_to_travel": unwilling_to_travel_public,
            "supporters": supporters_public,
        }
    })


def verify_signature(request, token):
    signature = get_object_or_404(models.Signature, token=token)

    if request.method == "POST":
        if request.POST.get("verify") == "true":
            signature.validated = True
            signature.save()
            messages.success(request, "Your signature has been verified.")
            return redirect("index")

    return render(request, "main/verify_signature.html")