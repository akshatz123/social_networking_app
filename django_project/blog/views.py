from django.shortcuts import render

posts = [
	{
		'author' : 'Akshat Zala',
		'title'  : 'Blog Post 1',
		'content': 'First Post content',
		'date_posted' : 'Aug 30, 2019'
	},
	{
		'author' : 'John Guttag',
		'title'  : 'Blog Post 2',
		'content': 'Second Post content',
		'date_posted' : 'Aug 31, 2019'
	}
]

def home(request):
	context={
		'posts': posts,
	}
	return render(request, 'blog/home.html', context)


def about(request):
	return render(request, 'blog/about.html', {'title':'About'})
