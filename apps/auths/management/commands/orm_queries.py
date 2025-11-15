#Python modules
from datetime import datetime, timedelta

#Django modules
from django.db.models import Q, Count, Avg, Max, Min, F, Value, Case, When, Sum, ExpressionWrapper, DecimalField
from django.db.models.functions import Concat, ExtractYear, Now

#Project modules 
from apps.auths.models import CustomUser as CU


# 1.Get all active users
active_users = CU.objects.filter(is_active=True)

# 2.Get users with a specific email domain
gmail_users = CU.objects.filter(email__endswith='@gmail.com')

# 3.Get users from Almaty
users_almaty = CU.objects.filter(city="Almaty")

# 4.Get users from not Almaty
not_almaty = CU.objects.exclude(city="Almaty")

# 5.Get users with salary greater than 500,000
salary_greater = CU.objects.filter(salary__gt=500000)

# 6.Get users with IT department in Kazakhstan
it_kz_users = CU.objects.filter(department="IT", country="Kazakhstan")

# 7.Get users with birth date is null
no_birth_date = CU.objects.filter(birth_date__isnull=True)

# 8.Get users whose name starts with "A"
first_name_a = CU.objects.filter(first_name__istartswith='A')

# 9.Get total number of users
total_users = CU.objects.count()

# 10.Get first 20 users ordered by date_joined desc
first_20_users = CU.objects.order_by('-created_at')[:20]

# 11.Get distinct list of city
distinct_list_of_city = CU.objects.values_list('city').distinct()

# 12.Get of users in Sales department
sales_users = CU.objects.filter(department="Sales").count()

# 13.Get all users logged in last 7 days
last_7_days = CU.objects.filter(last_login__gte=datetime.now()-timedelta(days=7))

# 14.Gt users with bek in first_name or last_name
bek_users = CU.objects.filter(Q(first_name__icontains="bek") | Q(last_name__icontains="bek"))

# 15.Get users whose salary between 300000 700000
salary_between = CU.objects.filter(salary__range=(300000,700000))

# 16.Get users whose departments in IT, HR, Finance
departments_in = CU.objects.filter(department__in=["IT", "HR", "Finance"])

# 17.Get users count group by department
group_by_department = CU.objects.values("department").annotate(user_counts=Count("id"))

# 18.Get users count group by department order by count desc
group_by_department = CU.objects.values('department').annotate(count=Count('id')).order_by('-count')

# 19. Get top 5 cities with most users
top_5_cities = CU.objects.values('city').annotate(count=Count('id')).order_by('-count')[:5]

# 20. Get users who never logged in
never_logged_in = CU.objects.filter(last_login__isnull=True)

# 21. Get average salary 
avg_salary = CU.objects.aggregate(avg=Avg('salary'))

# 22. Get max and min salary 
max_min_salary = CU.objects.aggregate(max_salary=Max('salary'), min_salary=Min('salary'))

# 23. Get users whose phone contains "+7"
phone_7 = CU.objects.filter(phone_number__contains='+7')

# 24. Annotate full_name
users_fullname = CU.objects.annotate(full_name=Concat(F('first_name'), Value(''), F('last_name')))

# 25. Annotate birth_year
users_birth_year = CU.objects.annotate(birth_year=ExtractYear('birth_date')).order_by('birth_year')

# 26. Users bown in May
born_may = CU.objects.filter(birth_date__month=5)

#27. Managers with salary > 400000
manager_salary = CU.objects.filter(role='manager', salary__gt=400000)

#28. Employees or department HR 
emp_or_hr = CU.objects.filter(Q(role='employee') | Q(department='HR'))

#29. Count active users per city 
active_per_city = CU.objects.filter(is_active=True).values('city').annotate(count=Count('id'))

#30. 10 earliest registered users 
earliest_10 = CU.objects.order_by('created_at')[:10]

#31. Get users whose city starts with 'A' and salary gt 300k
city_a_salary = CU.objects.filter(city__istartswith='A', salary__gt=300000)

#32.Users with empty or null department
empty_dep = CU.objects.filter(Q(department__isnull=True) | Q(department=''))

#33. Get stats by country: country name, num of users, and average salary per country
country_stats = CU.objects.values("country").annotate(count=Count('id'), avg_salary=Avg("salary"))

#34. is_staff = True ordered by last_login desc
staff_true_desc = CU.objects.filter(is_staff=True).order_by("-last_login")

#35. Users whose email does not contain "example.com"
not_example = CU.objects.exclude(email__icontains='example.com')

#36. Users whose salary gt avg salary
avg = CU.objects.aggregate(avg_salary=Avg("salary"))['avg_salary']
salary_gt_avg = CU.objects.filter(salary__gt=avg)

#37. Get emails used by more than one user
emails_used = CU.objects.values("email").annotate(count=Count("id")).filter(count__gt=1)

#38. 
users_salary_level = CU.objects.annotate(
    salary_level=Case(
    When(salary__lt=300000,then=Value('low')),
    When(salary__gte=300000, salary__lte=700000, then=Value('medium')),
    When(salary__gt=700000, then=Value('high')),
    default=Value('unkown')
    )).order_by('salary_level')

#39. Get users who joined this year
this_year=datetime.now().year
joined_this_year = CU.objects.filter(date_joined__year=this_year)

#40. Total salaries group by department
payroll_per_dept = CU.objects.values('department').annotate(total_salary=Sum('salary'))

#41. IT guys who never logged
it_never_login = CU.objects.filter(department="IT", last_login__isnull=True)

#42. Users whose country kz but country is null or empty 
kz_incomplete = CU.objects.filter(country='Kazakhstan').filter(Q(city__isnull=True) | Q(city=''))

#43. Users born before 1999-01-01 with null salary
born_before = CU.objects.filter(birth_date__lt='1990-01-01', salary__isnull=True)

#44.
users_years_since = CU.objects.annotate(years_since_joined=ExpressionWrapper((Now() - F('data_joined'))/365.25, output_field=DecimalField()))

#45. Users whose department sales email ends with @gmail.com and salary gt 350000
sales_gmail_salary = CU.objects.filter(department=('Sales'), email__endswith='@gmail.com', salary__gt=350000)

#46. Users ordered by country and in each country ordered by salary desc
users_ordered = CU.objects.order_by('country', '-salary')

#47. Get users count group by role where count gt 100  
role_stats = CU.objects.values('role').annotate(count=Count('id')).filter(count__gt=100)

#48. Users who login earlier than joined date
login_before_join = CU.objects.filter(last_login__lt=F('date_joined'))
 
#49. Get users whose birth date is lt 1985-01-01
users_senior = CU.objects.annotate(
  is_senior=Case(
   When(birth_date__lt='1985-01-01', then=Value(True)),
   default=Value(False)))

#50.departments sorted by avg salary desc where count gt 20
department_avg_salary = CU.objects.values('department').annotate(
    count=Count('id'),
    avg_salary=Avg('salary')
).filter(count__gte=20).order_by('-avg_salary')