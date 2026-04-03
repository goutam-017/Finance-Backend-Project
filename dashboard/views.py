from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum
from django.db.models.functions import TruncMonth,TruncWeek
from records.models import FinancialRecord
from users.permissions import IsAnalystOrAdmin

# Create your views here.
class DashboardSummaryView(APIView):
    permission_classes=[IsAnalystOrAdmin]

    def get(self,request):
        qs=FinancialRecord.objects.filter(is_deleted=False)

        total_income=qs.filter(type='income').aggregate(total=Sum('amount'))['total'] or 0
        total_expense=qs.filter(type='expense').aggregate(total=Sum('amount'))['total'] or 0
        net_balance=(total_income - total_expense)

        category_totals=(
            qs.values('category', 'type')
            .annotate(total=Sum('amount'))
            .order_by('category')
        )

        monthly_trends=(
            qs.annotate(month=TruncMonth('date'))
            .values('month', 'type')
            .annotate(total=Sum('amount'))
            .order_by('month')
        )

        weekly_trends=(
            qs.annotate(week=TruncWeek('date'))
            .values('week', 'type')
            .annotate(total=Sum('amount'))
            .order_by('week')
        )

        recent=qs.order_by('-date')[:5].values(
            'id', 'amount', 'type', 'category', 'date', 'description'
        )

        return Response({
            "total_income": total_income,
            "total_expense": total_expense,
            "net_balance": net_balance,
            "category_totals": list(category_totals),
            "monthly_trends": list(monthly_trends),
            "weekly_trends"   : list(weekly_trends),
            "recent_activity": list(recent),
        },status=status.HTTP_200_OK)