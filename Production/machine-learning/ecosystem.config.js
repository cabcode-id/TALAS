module.exports = {
  apps: [
    {
      name: "talas-ml",
      script: "/home/ubuntu/TALAS/Production/machine-learning/venv/bin/python3",
      args: "run.py",
      interpreter: "none",
      cwd: "/home/ubuntu/TALAS/Production/machine-learning",
      watch: false,
      autorestart: true,
      max_restarts: 5,
      env: {
        FLASK_ENV: "production",
      },
      out_file: "/home/ubuntu/.pm2/logs/talas-ml-out.log",
      error_file: "/home/ubuntu/.pm2/logs/talas-ml-error.log",
    }
  ]
};
