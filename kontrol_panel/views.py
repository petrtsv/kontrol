import json
from datetime import datetime, timedelta

from django.db import transaction
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt

from kontrol_panel.models import Session, Plot, Point, ImageData
from kontrol_panel.plotting.plotters import PlotlyPlotter

plotter = PlotlyPlotter()


def session_detail(request, session_id):
    session = get_object_or_404(Session, pk=session_id)
    plots = Plot.objects.filter(session=session.id)
    context = {
        'session': session,
        'plots': [plotter.to_html(plot) for plot in plots],
    }

    return render(request, 'kontrol_panel/session_view.html', context)


def index(request):
    active_sessions = Session.objects.order_by("-update_date").filter(status=Session.Status.STATUS_RUNNING,
                                                                      update_date__gt=datetime.now() - timedelta(
                                                                          hours=2))
    done_sessions = Session.objects.order_by("-update_date").filter(status=Session.Status.STATUS_DONE)

    context = {
        "active_sessions": active_sessions,
        "done_sessions": done_sessions
    }

    return render(request, 'kontrol_panel/index_view.html', context)


@csrf_exempt
def new_session(request):
    name = request.POST['name']
    session = Session(name=name)
    session.create_date = session.update_date
    session.save()
    return JsonResponse({'code': 200, 'result': {'id': str(session.id), 'token': str(session.token)}})


@csrf_exempt
def update_session(request):
    if 'session_token' not in request.POST:
        return HttpResponse('Unauthorized', status=401)

    session_token = request.POST['session_token']
    session = get_object_or_404(Session, token=session_token)

    if 'name' in request.POST:
        session.name = request.POST['name']

    if 'status' in request.POST:
        session.status = int(request.POST['status'])

    if 'progress' in request.POST:
        session.progress = float(request.POST['progress'])

    if 'millis_left' in request.POST:
        session.millis_left = int(float(request.POST['millis_left'])) * 1000

    session.update_date = datetime.now()

    session.save()
    return JsonResponse({'code': 200, 'result': {}})


@csrf_exempt
def new_plot(request):
    if 'session_token' not in request.POST:
        return HttpResponse('Unauthorized', status=401)

    session_token = request.POST['session_token']
    session = get_object_or_404(Session, token=session_token)

    title = request.POST['title']
    plot_type = int(request.POST['type'])
    plot = Plot(session=session, title=title, type=plot_type)
    plot.save()
    return JsonResponse({'code': 200, 'result': {'plot_id': plot.id}})


@csrf_exempt
def new_point(request):
    if 'session_token' not in request.POST:
        return HttpResponse('Unauthorized', status=401)
    if 'plot_id' not in request.POST:
        return HttpResponse('Bad request', status=402)
    if 'x' not in request.POST:
        return HttpResponse('Bad request', status=402)
    if 'y' not in request.POST:
        return HttpResponse('Bad request', status=402)
    if 'group' not in request.POST:
        return HttpResponse('Bad request', status=402)

    session_token = request.POST['session_token']
    session = get_object_or_404(Session, token=session_token)

    plot_id = int(request.POST['plot_id'])
    plot = get_object_or_404(Plot, id=plot_id)

    if plot.session_id != session.id:
        return HttpResponse('Unauthorized', status=401)

    x = float(request.POST['x'])
    y = float(request.POST['y'])
    group = str(request.POST['group'])

    point = Point(x_value=x, y_value=y, group=group, plot=plot)
    point.save()
    return JsonResponse({'code': 200, 'result': {}})


@csrf_exempt
def new_points(request):
    if 'session_token' not in request.POST:
        return HttpResponse('Unauthorized', status=401)
    if 'plot_id' not in request.POST:
        return HttpResponse('Bad request', status=402)
    if 'xs' not in request.POST:
        return HttpResponse('Bad request', status=402)
    if 'ys' not in request.POST:
        return HttpResponse('Bad request', status=402)
    if 'groups' not in request.POST:
        return HttpResponse('Bad request', status=402)

    session_token = request.POST['session_token']
    session = get_object_or_404(Session, token=session_token)

    plot_id = int(request.POST['plot_id'])
    plot = get_object_or_404(Plot, id=plot_id)

    if plot.session_id != session.id:
        return HttpResponse('Unauthorized', status=401)

    xs = json.loads(request.POST['xs'])
    ys = json.loads(request.POST['ys'])
    groups = json.loads(request.POST['groups'])
    with transaction.atomic():
        for x, y, group in zip(xs, ys, groups):
            if not Point.objects.filter(x_value=x, y_value=y, group=group, plot=plot).count():
                point = Point(x_value=x, y_value=y, group=group, plot=plot)
                point.save()
    return JsonResponse({'code': 200, 'result': {}})


@csrf_exempt
def new_image(request):
    if 'session_token' not in request.POST:
        return HttpResponse('Unauthorized', status=401)
    if 'plot_id' not in request.POST:
        return HttpResponse('Bad request', status=402)
    if 'image' not in request.FILES:
        return HttpResponse('Bad request', status=402)

    session_token = request.POST['session_token']
    session = get_object_or_404(Session, token=session_token)

    plot_id = int(request.POST['plot_id'])
    plot = get_object_or_404(Plot, id=plot_id)

    if plot.session_id != session.id:
        return HttpResponse('Unauthorized', status=401)

    image_data = ImageData(plot=plot, value=request.FILES['image'])
    image_data.save()

    return JsonResponse({'code': 200, 'result': {}})
