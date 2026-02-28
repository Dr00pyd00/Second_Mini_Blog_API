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

# commandes a exectuer 
COPY start.sh .
RUN chmod +x start.sh
CMD ["./start.sh"] 