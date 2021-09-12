from django.shortcuts import render
from django.http import HttpResponsePermanentRedirect, HttpResponse
import random
import string
import json

from share.models import Upload


def Index(request):
    """
    首页
    """
    if request.method == 'POST':  # 处理post请求
        if request.FILES:  # 确保有文件正在上传
            file = request.FILES.get('file')  # 获取文件对象
            name = file.name
            size = int(file.size)
            path = 'static/file/' + name
            uploads = Upload.objects.filter(name=name)
            if uploads:
                return render(request, 'repfile.html')
            with open(path, 'wb') as f:
                f.write(file.read())
            code = ''.join(random.sample(string.digits, 8))
            upload = Upload(
                path=path,
                name=name,
                filesize=size,
                code=code,
                pcip=str(request.META['REMOTE_ADDR'])
            )
            upload.save()
            return HttpResponsePermanentRedirect("/s/" + code)
        else:  # 没有选择文件就提示
            return render(request, 'nofile.html')
    else:
        return render(request, 'base.html')


def DisplayFiles(request, code):
    """
    文件列表显示
    """
    uploads = Upload.objects.filter(code=code)
    if uploads:
        for upload in uploads:
            upload.downloadcount += 1
            upload.save()
    return render(request, 'content.html', context={
        'content': uploads,
        'host': request.get_host()
    })


def FileManage(request):
    """
    文件管理
    """
    ip = request.META['REMOTE_ADDR']
    uploads = Upload.objects.filter(pcip=ip)
    for upload in uploads:
        upload.downloadcount += 1
        upload.save()
    return render(request, 'content.html', context={'content': uploads})


def SearchFile(request):
    """
    文件搜索
    """
    code = request.GET.get('kw')
    u = Upload.objects.filter(name__icontains=str(code))
    data = {}
    if u:
        # 将符合条件的数据放到 data 中
        for i in range(len(u)):
            u[i].save()
            data[i] = {}
            data[i]['download'] = u[i].downloadcount
            data[i]['filename'] = u[i].name
            data[i]['id'] = u[i].id
            data[i]['ip'] = str(u[i].pcip)
            data[i]['size'] = u[i].filesize
            data[i]['time'] = str(u[i].datetime.strftime('%Y-%m-%d %H:%M'))
            # 时间格式化
            data[i]['key'] = u[i].code
    # django 使用 HttpResponse 返回 json 的标准方式，content_type 是标准写法
    return HttpResponse(json.dumps(data), content_type="application/json")


def DownloadFile(request):
    """
    文件下载
    """


def Page404(request):
    """
    全局404页面
    """
    return render(request, '404.html', status=404)


def Page500(request):
    """
    全局500页面
    """
    return render(request, '500.html', status=500)
