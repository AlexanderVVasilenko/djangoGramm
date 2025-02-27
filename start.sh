echo "Starting DjangoGramm Deployment"

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Building frontend assets with Webpack..."
npm install -D webpack-cli
npm run build
npx webpack --mode production

echo "Collecting static files..."
python manage.py collectstatic --noinput