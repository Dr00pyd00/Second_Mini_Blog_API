# mini linux os with python only
FROM python:3.12-slim  

# Create directory inside the continer and cd in
WORKDIR /app

# copy requirements in the dir: so i's app/
COPY requirements.txt .

 # install the packages
 # No cache = less weight
 # RUN : during the Build
RUN pip install -r requirements.txt --no-cache-dir


# copy all project
# .: all of project   .: in cd container
COPY . . 

# say port where container listen
# 8000 = convention fastapi/uvicorn
EXPOSE 8000

# CMD something when container start running
# CMD: all time container start
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
