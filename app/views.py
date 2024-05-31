from django.shortcuts import render
# myapp/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Department, Post, PostImage
from django.utils import timezone
from django.contrib import messages
from django.http import HttpResponse
import datetime



@login_required
def department_list(request):
    departments = Department.objects.all()
    return render(request, 'application/department_list.html', {'departments': departments})

# @login_required
# def department_create(request):
#     if request.method == 'POST':
#         name = request.POST['name']
#         is_active = 'is_active' in request.POST
#         if Department.objects.filter(name=name).exists():
#             messages.error(request, "A department with this name already exists.")
#         Department.objects.create(name=name, created_by=request.user, created_on=timezone.now(), is_active=is_active)
#         return redirect('department_list')
#     return render(request, 'application/department_form.html')
@login_required
def department_create(request):
    if request.method == 'POST':
        name = request.POST['name']
        is_active = request.POST.get('is_active') == 'on'

        # Check if a department with the same name already exists
        if Department.objects.filter(name=name).exists():
            messages.error(request, "A department with this name already exists.")
        else:
            Department.objects.create(name=name, created_by=request.user,
                                      is_active=is_active)
            return redirect('department_list')

    return render(request, 'application/department_form.html')

@login_required
def department_delete(request, department_id):
    department = get_object_or_404(Department, id=department_id)
    if request.method == 'POST':
        department.delete()
        return redirect('department_list')
    return render(request, 'application/department_delete.html', {'department': department})


# post
# @login_required
# def post_create(request):
#     if request.method == 'POST':
#         title = request.POST['title']
#         description = request.POST['description']
#         images = request.FILES.getlist('image')
#         schedule_date = request.POST.get('schedule_date')
#         processed_date = request.POST.get('processed_date') or None
#         is_promoted = 'is_promoted' in request.POST
#
#         for image in images:
#             Post.objects.create(title=title, description=description, image=image, schedule_date=schedule_date,
#                                 processed_date=processed_date, is_promoted=is_promoted)
#         return redirect('post_list')
#     departments = Department.objects.all()
#     return render(request, 'application/post_form.html', {'departments': departments})
@login_required
def post_create(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        # images = request.FILES.getlist('images')
        schedule_date = request.POST.get('schedule_date')

        if schedule_date:
            try:
                schedule_date = datetime.datetime.strptime(schedule_date, '%Y-%m-%dT%H:%M')
                schedule_date = timezone.make_aware(schedule_date)
                # except ValueError:
                #     return HttpResponse('Invalid date format', status=400)  # Return a 400 Bad Request response

                if schedule_date < timezone.now():
                    return HttpResponse('Scheduled date cannot be in the past', status=400)
            except ValueError:
                return HttpResponse('Invalid date format', status=400)  # Return a 400 Bad Request response

        processed_date = request.POST.get('processed_date') or None
        is_promoted = 'is_promoted' in request.POST
        department_id = request.POST.get('department')

        try:
            department = Department.objects.get(id=department_id)
        except Department.DoesNotExist:
            return HttpResponse('Department does not exist', status=400)

        post = Post.objects.create(
            title=title,
            description=description,
            schedule_date=schedule_date,
            processed_date=processed_date,
            is_promoted=is_promoted,
            department=department
        )

        images = request.FILES.getlist('images')
        for image in images:
            PostImage.objects.create(post=post, image=image)
        return redirect('post_list')

    departments = Department.objects.all()
    return render(request, 'application/post_form.html', {'departments': departments})
@login_required
def post_list(request):
    if request.method == 'GET':
        # posts = Post.objects.all()
        posts = Post.objects.filter(is_deleted=False).order_by('-post_date')
        return render(request, 'application/post_list.html', {'posts': posts})

@login_required()
def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        post.is_deleted = True  # Mark the post as deleted
        post.save()
        return redirect('post_list')
    return render(request, 'application/post_delete.html', {'post': post})
#
@login_required
def post_update(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    departments = Department.objects.all()
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        schedule_date_str = request.POST.get('schedule_date')
        department_id = request.POST.get('department')
        department = Department.objects.get(id=department_id)

        # Update the post object with new values
        post.title = title
        post.description = description
        if schedule_date_str:
            try:
                schedule_date = timezone.datetime.strptime(schedule_date_str, '%Y-%m-%dT%H:%M')
            except ValueError:
                return HttpResponse('Invalid date format', status=400)

            if schedule_date < timezone.now():
                return HttpResponse('Scheduled date cannot be in the past', status=400)

            post.schedule_date = schedule_date

        image = request.FILES.getlist('images')
        if image:
            # images = PostImage.objects.filter(post=post)
            # for x in images:
            #     PostImage.objects.get(id=x.post_id).delete()
            for y in image:
                PostImage.objects.create(post=post, image=y).save()

        post.is_promoted = request.POST.get('is_promoted') == '1'
        post.department = department
        post.save()

        return redirect('post_list')

    return render(request, 'application/post_form.html', {'post': post, 'departments': departments})

@login_required
def dashboard(request):
    total_posts = Post.objects.count()
    total_images = Post.objects.exclude(image='').count()
    paid_posts = Post.objects.filter(is_promoted=True).count()
    unpaid_posts = Post.objects.filter(is_promoted=False).count()

    context = {
        'total_posts': total_posts,
        'total_images': total_images,
        'paid_posts': paid_posts,
        'unpaid_posts': unpaid_posts,
    }
    return render(request, 'registration/dashboard.html', context)

@login_required
def delete_post_image(request, image_id):
    image = get_object_or_404(PostImage, id=image_id)
    post = image.post
    if request.method == 'POST':
        image.delete()
        return redirect('post_update', post_id=post.id)  # Redirect back to the post update page or wherever you want

    return render(request, 'application/delete_image.html', {'image': image})