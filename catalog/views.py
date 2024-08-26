from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.forms import inlineformset_factory
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from pytils.translit import slugify

from catalog.forms import ProductForm, VersionForm, ProductModeratorForm
from catalog.models import Product, Version
from catalog.services import get_products_from_cache


@login_required
def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(f'You have new message from {name}({email}): {message}')
    return render(request, 'main/contact.html')

class ProductCreateView(CreateView, LoginRequiredMixin):
    model = Product
    form_class = ProductForm
    template_name = ('main/product_form.html')
    success_url = reverse_lazy('catalog:product_list')

    def form_valid(self, form):
        product = form.save()
        user = self.request.user
        product.owner = user
        product.save()
        if form.is_valid():
            product = form.save()
            product.slug = slugify(product.product)
            product.save()
        return super().form_valid(form)


class ProductUpdateView(UpdateView, LoginRequiredMixin):
    model = Product
    form_class = ProductForm
    template_name = ('main/product_form.html')

    def get_success_url(self):
        return reverse('catalog:product_view', args=[self.kwargs.get('pk')])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = VersionFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)

    def get_form_class(self):
        user = self.request.user

        if user == self.object.owner or user.has_perm('catalog.change_product') and user.has_perm(
                'catalog.delete_product'):
            return ProductForm

        if user.has_perm("catalog.can_edit_category") and user.has_perm(
            "catalog.can_edit_description") and user.has_perm(
            "catalog.can_edit_is_published"):
            return ProductModeratorForm

        raise PermissionDenied


class ProductDeleteView(DeleteView, LoginRequiredMixin):
    model = Product
    template_name = ('main/product_delete.html')
    success_url = reverse_lazy('catalog:product_list')

    def get_success_url(self):
        return reverse('catalog:product_list')

class ProductListView(ListView):
    model = Product
    template_name = ('main/product_list.html')


    def get_queryset(self):
        return get_products_from_cache()

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        products = self.get_queryset()
        for product in products:
            product.version = product.version_set.filter(is_current=True).first()

        context_data['object_list'] = products
        return context_data


class ProductDetailView(DetailView, LoginRequiredMixin):
    model = Product
    template_name = ('main/product_detail.html')
    permission_required = 'catalog.product_view'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.view_counter += 1
        self.object.save()
        return self.object

    # def get_object(self, queryset=None):
    #     self.object = super().get_object(queryset)
    #     if self.request.user == self.object.owner:
    #         self.object.view_counter += 1
    #         self.object.save()
    #         return self.object
    #     raise PermissionDenied
