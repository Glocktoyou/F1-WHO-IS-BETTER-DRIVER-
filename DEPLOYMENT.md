# 🚀 Deployment Guide

This guide will help you deploy your F1 WHO IS BETTER DRIVER? application to various cloud platforms.

## 🌐 Quick Deploy Options

### Option 1: Render (Recommended - Free Tier)

1. **Fork/Clone** this repository to your GitHub account
2. **Visit** [render.com](https://render.com) and sign up
3. **Create New Web Service** and connect your GitHub repository
4. **Configure Settings:**
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn src.app:app --bind 0.0.0.0:$PORT`
   - **Environment:** Python 3.10+
   - **Auto-Deploy:** Yes

Your app will be live at: `https://your-app-name.onrender.com`

### Option 2: Heroku

1. **Install** Heroku CLI and login: `heroku login`
2. **Create app:** `heroku create your-f1-app-name`
3. **Deploy:**
   ```bash
   git push heroku main
   ```
4. **Open:** `heroku open`

### Option 3: Railway

1. **Visit** [railway.app](https://railway.app) 
2. **Connect** your GitHub repository
3. **One-click deploy** - Railway auto-detects Python apps
4. **Custom domain** available on paid plans

### Option 4: Vercel (Serverless)

1. **Install** Vercel CLI: `npm i -g vercel`
2. **Deploy:** `vercel --prod`
3. **Follow** the prompts

## 🔧 Platform-Specific Configuration

### Render Configuration

Create `render.yaml` (optional):
```yaml
services:
  - type: web
    name: f1-analysis
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn src.app:app --bind 0.0.0.0:$PORT
    envVars:
      - key: PYTHON_VERSION
        value: 3.10.5
```

### Heroku Configuration

The included `Procfile` handles Heroku deployment:
```
web: gunicorn src.app:app --bind 0.0.0.0:$PORT
```

### Environment Variables

Set these environment variables in your deployment platform:

| Variable | Value | Description |
|----------|-------|-------------|
| `PYTHON_VERSION` | `3.10.5` | Python version |
| `PORT` | `5000` | Port (usually auto-set) |
| `FLASK_ENV` | `production` | Flask environment |

## 🏠 Local Production Setup

### Using Gunicorn (Recommended)

```bash
# Install Gunicorn
pip install gunicorn

# Run production server
gunicorn --bind 0.0.0.0:5000 --workers 4 src.app:app

# With specific configuration
gunicorn --config gunicorn.conf.py src.app:app
```

### Create gunicorn.conf.py:
```python
bind = "0.0.0.0:5000"
workers = 4
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
timeout = 30
keepalive = 2
```

### Using Docker (Optional)

Create `Dockerfile`:
```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "src.app:app"]
```

Build and run:
```bash
docker build -t f1-analysis .
docker run -p 5000:5000 f1-analysis
```

## ⚡ Performance Optimization

### For Production Deployments:

1. **Enable Caching**
   - FastF1 cache is already configured
   - Consider Redis for session caching

2. **Optimize Dependencies**
   - Use `--no-dev` flag when installing
   - Consider `gunicorn[gevent]` for async support

3. **Environment Configuration**
   ```bash
   export FLASK_ENV=production
   export PYTHONPATH=/app/src
   ```

4. **Static File Serving**
   - Use CDN for static assets in production
   - Configure nginx for static file serving (if using VPS)

## 🔐 Security Considerations

### Production Security Checklist:

- [ ] Set `FLASK_ENV=production`
- [ ] Use HTTPS (most platforms provide this automatically)
- [ ] Set secure session configuration
- [ ] Enable CSRF protection if adding forms
- [ ] Configure CORS if needed for API access
- [ ] Regular dependency updates

### Example Production Flask Config:
```python
# In src/app.py, add production config
import os

if os.environ.get('FLASK_ENV') == 'production':
    app.config.update(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'your-secret-key'),
        SESSION_COOKIE_SECURE=True,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE='Lax',
    )
```

## 📊 Monitoring & Logs

### View Logs:

**Render:**
```bash
# View logs in dashboard or CLI
render logs --service your-service-name
```

**Heroku:**
```bash
heroku logs --tail
```

**Railway:**
```bash
railway logs
```

### Health Checks:

Add to your Flask app:
```python
@app.route('/health')
def health_check():
    return {'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()}
```

## 🚨 Troubleshooting

### Common Issues:

1. **Memory Errors**
   - Reduce FastF1 cache size
   - Use worker processes instead of threads
   - Consider upgrading to paid plan

2. **Slow Performance**
   - Enable FastF1 caching
   - Use persistent storage for cache
   - Optimize matplotlib backend (already set to 'Agg')

3. **Import Errors**
   - Check `PYTHONPATH` includes `src/`
   - Verify all dependencies are installed
   - Check Python version compatibility

4. **Static Files Not Loading**
   - Verify static file paths in templates
   - Check Flask static folder configuration
   - Consider using CDN for production

### Debug Commands:
```bash
# Check if app imports correctly
python -c "from src.app import app; print('App loaded successfully')"

# Test local gunicorn
gunicorn --check-config src.app:app

# Verify dependencies
pip check
```

## 🎯 Post-Deployment

After successful deployment:

1. **Update README** with your live URL
2. **Test all features** (web interface, visualizations, exports)
3. **Monitor performance** and logs
4. **Set up monitoring** (optional: UptimeRobot, etc.)
5. **Share your deployment** with the F1 community!

## 📞 Support

If you encounter issues during deployment:

1. Check the platform-specific documentation
2. Review application logs for errors
3. Verify all environment variables are set
4. Test locally with Gunicorn first
5. Open an issue on GitHub with deployment details

---

**Happy Racing! 🏎️** Your F1 analysis tool is now ready for the world!