module.exports = {
  apps: [
    {
      name: 'my-python-bot2',
      script: 'main.py',
      interpreter: 'python3',
      watch: false, // Установите в true, если хотите, чтобы PM2 перезапускал скрипт при изменениях
      autorestart: true,
      env: {
        // Здесь можно задать переменные окружения, если необходимо
        PYTHONPATH: '.env',
      },
    },
  ],
};
