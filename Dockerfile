FROM python:3.10-slim-bullseye

# إعداد البيئة
ENV PYTHONUNBUFFERED=1

# تثبيت الاعتماديات الأساسية في خطوة واحدة
RUN apt-get update && apt-get install -y libcairo2-dev gcc && apt-get clean

# تعيين مجلد العمل
WORKDIR /app/

# نسخ فقط ملف المتطلبات أولاً لتقليل عدد العمليات عند التغيير في الملفات الأخرى
COPY requirements.txt /app/

# تثبيت الحزم
RUN pip install --no-cache-dir -r requirements.txt

# نسخ باقي الملفات بعد تثبيت الحزم
COPY . /app/

# منح صلاحيات التنفيذ لملف entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# كشف المنفذ 8000
EXPOSE 8000

# تشغيل السيرفر
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "horilla.wsgi:application"]
