# EZ Play — Ficha da Google Play

## Textos da loja (Play Console → Presença na loja → Página principal da loja)

**Nome do app** (24/30)
```
EZ Play – Player de IPTV
```

**Descrição curta** (69/80)
```
Player para suas playlists M3U e Xtream: TV ao vivo, filmes e séries.
```

**Descrição completa** (1.922/4.000)
```
EZ Play é o player simples e bonito para assistir às suas próprias playlists no celular, no tablet e na TV.

Adicione sua playlist em segundos e tenha seus canais ao vivo, filmes e séries organizados em uma tela inicial moderna, com capas, destaques e categorias.

★ COMO FUNCIONA
O EZ Play é um reprodutor (player). Você adiciona a playlist que já possui, fornecida pelo seu provedor, e assiste com uma interface organizada e fácil de usar.

★ FORMAS DE ADICIONAR SUA PLAYLIST
• Login no padrão Xtream Codes (servidor, usuário e senha)
• Link de playlist M3U / M3U8
• Arquivo .m3u salvo no aparelho
• Link direto de um canal ou vídeo

★ TV AO VIVO
• Canais organizados por categoria
• Troca rápida de canal pelo controle remoto (▲ ▼ ou CH+ / CH−)
• Favoritos para chegar rápido aos canais preferidos
• Busca por nome

★ FILMES E SÉRIES
• Capas, nota, ano, gênero e sinopse (quando informados pelo provedor)
• Séries com temporadas e episódios
• Próximo episódio automático
• Continuar assistindo: volte de onde parou
• Lista "Assistir depois"

★ PARA A FAMÍLIA TODA
• Perfis separados, cada um com seus favoritos e histórico
• Controle parental com PIN para ocultar conteúdo adulto

★ FUNCIONA NA SUA TV
• Celular, tablet, Android TV e TV Box
• Navegação completa pelo controle remoto
• Player de alto desempenho com suporte a HLS (m3u8), MPEG-TS, MP4 e MKV

★ PRIVACIDADE
Suas playlists e preferências ficam salvas apenas no seu aparelho. O EZ Play não exige cadastro e não coleta dados pessoais.

★ QUER CONHECER ANTES?
Toque em "Experimentar com vídeos de demonstração" e assista a filmes de licença aberta para conhecer o app.

IMPORTANTE: o EZ Play não fornece, não vende e não inclui nenhum canal, filme, série ou playlist. O app apenas reproduz o conteúdo adicionado pelo próprio usuário. Use somente playlists e conteúdos que você tem direito de acessar. O EZ Play não tem vínculo com nenhum provedor de conteúdo.
```

## Imagens (pasta `store/`)
| Campo do Play Console | Arquivo |
|---|---|
| Ícone do app (512×512) | `icon-512.png` |
| Recurso gráfico (1024×500) | `feature-1024x500.png` |
| Capturas de tela do telefone (2 a 8) | `celular-1.png` … `celular-6.png` (1080×1920) |
| Capturas de tela da Android TV | `tv-1.png` … `tv-4.png` (1920×1080) |
| Banner da Android TV (já no app) | `android/app/src/main/res/drawable-xhdpi/banner.png` |

As telas usam títulos e canais fictícios, sem nenhuma marca real.

## Detalhes do app
- **Categoria:** Players e editores de vídeo
- **Tags sugeridas:** Player de vídeo, Streaming, TV
- **Política de privacidade:** https://ezplaytv.vercel.app/privacidade.html
- **Site:** https://ezplaytv.vercel.app
- **E-mail de contato:** obrigatório. Use um e-mail profissional da marca, não o pessoal.

## Respostas dos formulários (Play Console → Política e programas → Conteúdo do app)

**Acesso ao app**
- Escolha: "Todas ou algumas funcionalidades estão restritas" → adicione a instrução:
  > O app é um player e não inclui conteúdo. Para testar, abra o app e toque em "Experimentar com vídeos de demonstração" na tela inicial. Isso carrega filmes de licença aberta (Blender Foundation) e canais de teste HLS públicos. Nenhum login é necessário.

**Anúncios:** Não, o app não contém anúncios.

**Segurança dos dados**
- O app coleta ou compartilha dados do usuário? **Não.**
- Justificativa: playlists, perfis, favoritos e progresso ficam armazenados apenas no aparelho e nunca são enviados ao desenvolvedor.
- Os dados são criptografados em trânsito? As conexões são feitas diretamente aos servidores das playlists do usuário.
- O usuário pode pedir exclusão? Sim: Configurações → Apagar todos os dados deste aparelho, ou desinstalando.

**Classificação do conteúdo (questionário IARC)**
- Categoria: "Utilitários, produtividade, comunicação ou outro".
- O app não tem violência, sexo, linguagem imprópria, drogas, jogos de azar nem compras.
- Pergunta sobre conteúdo gerado ou fornecido pelo usuário / acesso à internet sem filtro: **Sim**, o app reproduz conteúdo de playlists adicionadas pelo usuário (com controle parental por PIN).

**Público-alvo:** 18 anos ou mais (evita as exigências extras da política de apps para crianças).

**App de notícias:** Não. **Apps governamentais:** Não. **Recursos financeiros:** Não. **Saúde:** Não.

**Android TV**
- Em "Configuração avançada → Formatos", adicione **Android TV** e envie as capturas `tv-*.png`.
- O app já tem banner, categoria LEANBACK e funciona 100% pelo controle remoto.

## O que costuma reprovar apps de IPTV (evite)
- Citar marcas de canais, emissoras, ligas esportivas ou streamings na descrição ou nas imagens.
- Prometer "TV grátis", "todos os canais" ou filmes de cinema.
- Prints mostrando conteúdo protegido (filmes reais, logos de canais).
- Divulgar o app junto com venda de listas.

## Teste fechado (contas pessoais novas)
Antes de publicar para todos, o Google exige **12 testadores ativos por 14 dias** em teste fechado.
Convide clientes e amigos pelo e-mail Google deles; eles instalam pelo link de teste da Play Store.
