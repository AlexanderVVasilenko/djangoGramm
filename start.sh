echo "Starting DjangoGramm Deployment"

if [ ! -d "venv" ]; then
  echo "Virtual environment 'venv' not found. Creating one..."
  python -m venv venv
fi

if [ -f "venv/bin/activate" ]; then
  source venv/bin/activate
elif [ -f "venv/Scripts/activate" ]; then
  source venv/Scripts/activate
else
  echo "Error: Virtual environment activation script not found."
  exit 1
fi

echo "Virtual environment activated"

echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Building frontend assets with Webpack..."
npm install -D webpack-cli
npm run build
npx webpack --mode production