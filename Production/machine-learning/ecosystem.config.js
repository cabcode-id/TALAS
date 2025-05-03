module.exports = {
  apps: [
    {
      name: "talas-ml",
      script: "run.py",
      interpreter: "/home/ubuntu/venv/bin/python3",
      cwd: "/home/ubuntu/TALAS/Production/machine-learning",
      watch: false,
      autorestart: true,
      max_restarts: 5,
      env: {
        FLASK_ENV: "production"
      }
    }
  ]
}
