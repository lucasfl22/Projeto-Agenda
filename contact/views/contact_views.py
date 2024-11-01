from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from contact.models import Contact
from django.http import Http404

def index(request):
    contacts = Contact.objects.all().filter(show=True).order_by('-id')
    paginator = Paginator(contacts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'contact/index.html', {'page_obj': page_obj})


def search(request):
    search_value = request.GET.get('q', '').strip()
    
    if search_value == '':
        return redirect('contact:index')
    
    search_words = search_value.split()
    
    if len(search_words) > 1:
        contacts = Contact.objects.filter(show=True,first_name__icontains=search_words[0],last_name__icontains=search_words[-1])
    else:
        contacts = Contact.objects.filter(show=True).filter(Q(first_name__icontains=search_value) | Q(last_name__icontains=search_value) | Q(phone__icontains=search_value) | Q(email__icontains=search_value))
        
    paginator = Paginator(contacts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'contact/index.html', {'page_obj': page_obj, 'search_value': search_value})



def contact(request, contact_id):
    single_contact = get_object_or_404(Contact, pk=contact_id, show=True)
    
    context = {
        'contact': single_contact,
    }
    
    return render(request, 'contact/contact.html', context)
