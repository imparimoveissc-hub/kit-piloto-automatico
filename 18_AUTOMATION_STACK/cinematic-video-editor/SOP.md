# SOP — Editar vídeo cinematográfico

## Entrada

- Vídeo bruto em `.mp4`, `.mov` ou `.webm`.
- Opcional: legenda `.srt` ou `.vtt`.
- Opcional: indicação de formato:
  - `cinematic-reels` para Reels/Stories/TikTok;
  - `clean-reels` para visual mais limpo;
  - `wide-cinematic` para YouTube/horizontal.

## Procedimento

1. Colocar o vídeo em uma pasta local acessível.
2. Rodar o editor:

```bash
python3 18_AUTOMATION_STACK/cinematic-video-editor/cinematic_editor.py "/caminho/video.mp4" --auto-cut
```

3. Conferir o MP4 final em `06_OUTPUTS/cinematic-video-editor/<video>/`.
4. Conferir `relatorio.md`.
5. Se houver legenda, repetir com `--subtitles`.

## Critérios de qualidade

- Rosto/assunto principal não pode ficar cortado de forma estranha.
- Legenda não pode cobrir boca, produto ou informação importante.
- Cortes automáticos não podem cortar palavras.
- Áudio precisa ficar audível sem estourar.
- Se o vídeo for comercial/imobiliário, não inserir promessa sem prova.

## Rollback

- O vídeo original nunca é alterado.
- Arquivos temporários ficam em `_work/`.
- Para desfazer, apagar a pasta de saída.

