import json
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import generics
from .models import Expense
from .serializers import ExpenseSerializer
from .forms import ExpenseForm
from datetime import datetime
from expense import models
from django.db.models import Sum
from django.db.models.functions import TruncMonth


class ExpenseListCreateAPIView(generics.ListCreateAPIView):
    queryset = Expense.objects.all().order_by('-date')
    serializer_class = ExpenseSerializer


class ExpenseRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer


def expense_dashboard(request, pk=None):
    try:
        expenses = Expense.objects.all().order_by('-date')
        total_amount = sum(exp.amount for exp in expenses)
        date_range = request.GET.get('date_range')

        if date_range and "to" in date_range:
            try:
                start_str, end_str = date_range.split(" to ")
                start_date = datetime.strptime(
                    start_str.strip(), "%Y-%m-%d").date()
                end_date = datetime.strptime(
                    end_str.strip(), "%Y-%m-%d").date()
                expenses = expenses.filter(date__range=(start_date, end_date))
                total_amount = expenses.aggregate(
                    total=Sum('amount'))['total'] or 0
            except:
                pass

        # Monthly totals
        monthly_data = (
            expenses
            .annotate(month=TruncMonth('date'))
            .values('month')
            .annotate(total=Sum('amount'))
            .order_by('month')
        )
        chart_labels = [entry['month'].strftime(
            '%b %Y') for entry in monthly_data]

        # Convert Decimal to float here!
        chart_data = [float(entry['total']) for entry in monthly_data]

        if pk:
            expense = get_object_or_404(Expense, pk=pk)
            form = ExpenseForm(request.POST or None, instance=expense)
            if request.method == 'POST' and form.is_valid():
                form.save()
                return redirect('expense-dashboard')
        else:
            form = ExpenseForm(request.POST or None)
            if request.method == 'POST' and form.is_valid():
                form.save()
                return redirect('expense-dashboard')

        context = {
            'expenses': expenses,
            'form': form,
            'edit_id': pk,
            'total_amount': total_amount,
            'chart_labels_json': json.dumps(chart_labels),
            'chart_data_json': json.dumps(chart_data),
        }
    except Exception as isoex:
        print(isoex)

    return render(request, 'dashboard.html', context)


def delete_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    expense.delete()
    return redirect('expense-dashboard')
