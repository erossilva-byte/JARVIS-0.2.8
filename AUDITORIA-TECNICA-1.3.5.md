# J.A.R.V.I.S. Nova — auditoria técnica e plano de estabilização

Data da auditoria: 2026-10-19
Base examinada: branch `main`, commit `a9caeefa7fb648170271a4168b1e1ff53ff966bd`, workflow `.github/workflows/build-apk.yml` e arquivo de fonte `JARVIS-NOVA-1.3.4-fonte.zip`.

## Estado comprovado

- O repositório contém o fonte versionado como ZIP; o workflow extrai esse arquivo antes de compilar.
- O workflow executa verificações JavaScript/Python e testes de regressão antes de gerar o APK.
- A compilação atual substitui `JarvisLocalAIPlugin.java` por um stub de compatibilidade e remove a dependência MediaPipe GenAI. Portanto, **a IA local não está funcional nesta compilação**, mesmo que o APK seja gerado com sucesso.
- O próprio workflow registra incompatibilidade entre o bytecode do MediaPipe GenAI 0.10.27 (Java 21) e o JDK 17 configurado, além de uma referência de API incompatível com Capacitor 6.
- O artefato atual é uma compilação debug. Não deve ser tratado como lançamento assinado para distribuição.

## Prioridades para a próxima versão

### P0 — Integridade e compilação reproduzível
1. Parar de alterar/substituir código-fonte da aplicação silenciosamente durante a compilação; tornar patches explícitos, versionados e testados.
2. Separar testes web, testes de plugins nativos e testes de empacotamento.
3. Registrar versões exatas de Node, npm, Capacitor, Gradle, Android Gradle Plugin e dependências.
4. Gerar APK e checksum, e guardar logs legíveis quando o build falhar.
5. Validar permissões e componentes Android do manifesto contra os plugins realmente presentes.

### P1 — Voz sem serviço pago obrigatório
1. Manter reconhecimento de fala pt-BR por meio do serviço de reconhecimento do Android quando disponível, com mensagens claras quando o mecanismo ou pacote de idioma não estiver instalado.
2. Separar três funções distintas: reconhecimento de fala, palavra de ativação local e identificação de locutor. Não anunciar identificação de locutor sem implementação e teste específicos.
3. Para palavra de ativação, avaliar primeiro uma implementação local compatível com Android/JDK e licença adequada. Não deixar o microfone continuamente ativo sem consentimento explícito, indicação visível e controle para desligar.
4. Testar interrupção de TTS, ruído, permissões negadas, ausência de rede, tela bloqueada e consumo de bateria antes de declarar o recurso pronto.

### P2 — Ações do telefone com consentimento
1. Implementar cada ação Android como uma capacidade independente, com permissão mínima e fallback seguro.
2. Para notificações, exigir que o usuário habilite manualmente o acesso especial do Android; permitir revogação e explicar o que é lido.
3. Para chamadas, SMS, contatos, alarmes e abertura de apps, confirmar a ação quando houver ambiguidade ou efeito externo.
4. Nunca coletar mensagens, notificações, contatos ou e-mails sem uma ação clara do usuário e permissões apropriadas.

### P3 — Interface e manutenção
1. Padronizar componentes, estados de carregamento/erro/vazio e tamanhos de texto.
2. Garantir navegação acessível, contraste, feedback para microfone ativo e controles visíveis de parar/fechar.
3. Separar lógica de interface, serviços de IA, voz, memória e integração Android.
4. Não armazenar chaves de API em código versionado; oferecer armazenamento local e opção de apagar dados.

## Critérios mínimos de aceite

- O build passa sem substituir funcionalidades reais por stubs sem aviso.
- Testes cobrem o caminho feliz e falhas de permissões, rede, APIs e serviços de voz.
- A tela de voz informa o estado real: aguardando, ouvindo, processando, falando, erro ou desativado.
- O app não promete ativação por palavra-chave em segundo plano até que isso tenha sido demonstrado em aparelho físico.
- Toda permissão especial é explicada e pode ser revogada pelo usuário.
- APK final é instalado e validado num dispositivo Android real; build verde sozinho não prova funcionamento em uso.

## Limite desta auditoria

Este documento registra apenas os pontos confirmados no repositório e no workflow. Não afirma que recursos ainda não testados foram implementados. As próximas alterações de interface e plugins devem ser feitas contra os arquivos de fonte extraídos e verificadas por testes e build.
