import React, { useState } from "react";
import axios from "axios";
import { Button, TextField, Select, MenuItem, Typography, Container, Box, CircularProgress } from "@mui/material";

function Home() {
  const [url, setUrl] = useState("");
  const [outputType, setOutputType] = useState("Patentes");
  const [processing, setProcessing] = useState(false);  // Para controlar o status do processamento
  const [statusMessage, setStatusMessage] = useState("");  // Para exibir a mensagem de status

  const handleSubmit = async (e) => {
    e.preventDefault();

    setProcessing(true);  // Inicia o processamento
    setStatusMessage("Processamento iniciado, aguarde...");

    try {
      const response = await axios.post("http://127.0.0.1:5000/process", {
        url,
        output_type: outputType,
      });

      // Se a resposta for recebida com sucesso, mostra a mensagem que o processamento foi iniciado
      setStatusMessage(response.data.message);
      
      // Aqui pode ser inserido um timer ou outro mecanismo para verificar quando o processo foi concluído, se necessário.
      // Exemplo de simulação de conclusão após 10 segundos
      setTimeout(() => {
        setProcessing(false);
        setStatusMessage("Processamento concluído!");
      }, 10000);  // Simulação de conclusão após 10 segundos
    } catch (error) {
      setProcessing(false);  // Para o processo
      setStatusMessage("Erro ao processar!");
    }
  };

  return (
    <Container className="min-h-screen flex flex-col items-center justify-center bg-gray-900 text-white">
      <Typography variant="h3" className="text-primary font-bold mb-2">
        🚀 Gerador de Portfólio
      </Typography>
      <Typography variant="subtitle1" className="text-gray-400 mb-6">
        Transforme informações em materiais profissionais.
      </Typography>

      <Box className="bg-gray-800 p-8 rounded-lg shadow-lg w-full max-w-md">
        <form onSubmit={handleSubmit} className="space-y-6">
          <TextField
            fullWidth
            label="🔗 Link da Vitrine"
            variant="outlined"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="Cole o link aqui..."
            required
            className="bg-gray-700 text-white rounded-lg"
          />

          <Select
            fullWidth
            value={outputType}
            onChange={(e) => setOutputType(e.target.value)}
            variant="outlined"
            className="bg-gray-700 text-white rounded-lg"
          >
            <MenuItem value="Patentes">📜 Patentes</MenuItem>
            <MenuItem value="Softwares">💻 Softwares</MenuItem>
            <MenuItem value="Serviços">🛠️ Serviços</MenuItem>
            <MenuItem value="Pesquisas">🔬 Pesquisas</MenuItem>
            <MenuItem value="Laboratórios">🏢 Laboratórios</MenuItem>
          </Select>

          <Button
            type="submit"
            variant="contained"
            fullWidth
            className="bg-primary hover:bg-primary-dark py-3 mt-4 rounded-lg font-bold"
          >
            ⚡ Processar
          </Button>
        </form>
      </Box>

      <Box className="mt-4">
        {processing ? (
          <CircularProgress color="secondary" />
        ) : (
          <Typography variant="h6" className="text-gray-400 mt-4">{statusMessage}</Typography>
        )}
      </Box>

      <footer className="mt-8 text-center text-gray-400">
        <Typography variant="body2">
          Desenvolvido por <strong>André</strong> | Universidade Estadual do Norte do Paraná - UENP
        </Typography>
        <Typography variant="body2">
          📧 Email: andre@email.com | 📍 UENP - Campus de Computação
        </Typography>
      </footer>
    </Container>
  );
}

export default Home;
