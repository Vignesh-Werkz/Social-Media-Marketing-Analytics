# Run docker build from the project root, outside the /src folder
# Use: docker build -t datalyzer-datamanagement -f src/datamanagement/Dockerfile .

FROM python:3.11.9
COPY src/datamanagement/DMrequirements.txt .
RUN pip install -r DMrequirements.txt
COPY src/DMMain.py .
COPY src/datamanagement ./datamanagement/
ENTRYPOINT ["python", "DMMain.py"]
EXPOSE 443/tcp