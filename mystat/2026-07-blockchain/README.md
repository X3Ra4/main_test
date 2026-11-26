# Навчальний Blockchain
`python miner_demo.py` показує пошук nonce, два блоки з транзакціями та відхилення підміни. Для мережевого прикладу запустіть окремо `python node.py --port 8011 --peer http://127.0.0.1:8012` та `python node.py --port 8012 --peer http://127.0.0.1:8011`.

```bash
curl -X POST http://127.0.0.1:8011/transaction -H 'Content-Type: application/json' -d '{"text":"Alice -> Bob: 5"}'
curl -X POST http://127.0.0.1:8011/mine
curl http://127.0.0.1:8012/chain
curl -X POST http://127.0.0.1:8012/sync
```

Вузли працюють окремими процесами, чергою mempool і майнінгом керують окремі потоки. Транзакції, що не ввійшли в блок, залишаються у черзі. Після заміни ланцюга непідтверджені транзакції попередньої гілки повертаються в mempool. Усі транзакції демонстраційні.
