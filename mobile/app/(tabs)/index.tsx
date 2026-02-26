import React, { useEffect, useState, useCallback } from 'react';
import { View, Text, FlatList, StyleSheet, ActivityIndicator, TouchableOpacity, RefreshControl } from 'react-native';

// 1. Criamos a "Interface" para o TypeScript parar de dar erro no 'item'
interface Aparelho {
  id: number;
  modelo: string;
  imei: string;
  numero_serie: string;
  status: string;
}

export default function HomeScreen() {
  // 2. Definimos que a lista será do tipo Aparelho[]
  const [aparelhos, setAparelhos] = useState<Aparelho[]>([]);
  const [carregando, setCarregando] = useState(true);
  const [atualizando, setAtualizando] = useState(false);

  const buscarDados = async () => {
    try {
      // 10.0.2.2 é o IP para o emulador falar com o seu PC
      const response = await fetch('http://10.0.2.2:5000/aparelhos');
      const data = await response.json();
      setAparelhos(data);
    } catch (error) {
      console.error("Erro na API:", error);
    } finally {
      setCarregando(false);
      setAtualizando(false);
    }
  };

  const aoAtualizar = useCallback(() => {
    setAtualizando(true);
    buscarDados();
  }, []);

  useEffect(() => {
    buscarDados();
  }, []);

  if (carregando) {
    return <ActivityIndicator size="large" color="#007AFF" style={styles.centro} />;
  }

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.titulo}>📱 Dispositivos</Text>
        <TouchableOpacity style={styles.botaoAtualizar} onPress={buscarDados}>
          <Text style={styles.textoBotao}>Atualizar</Text>
        </TouchableOpacity>
      </View>
      
      <FlatList
        data={aparelhos}
        keyExtractor={(item) => item.id.toString()}
        refreshControl={
          <RefreshControl refreshing={atualizando} onRefresh={aoAtualizar} />
        }
        renderItem={({ item }) => (
          <View style={styles.card}>
            <View style={styles.info}>
              <Text style={styles.modelo}>{item.modelo}</Text>
              <Text style={styles.detalhe}>S/N: {item.numero_serie}</Text>
              <Text style={styles.detalhe}>IMEI: {item.imei}</Text>
            </View>
            <View style={[styles.badge, { backgroundColor: item.status === 'Disponível' ? '#dcfce7' : '#fee2e2' }]}>
              <Text style={{ color: item.status === 'Disponível' ? '#166534' : '#991b1b', fontWeight: 'bold' }}>
                {item.status}
              </Text>
            </View>
          </View>
        )}
        ListEmptyComponent={<Text style={styles.vazio}>Nenhum aparelho encontrado.</Text>}
      />
    </View>
  );
}

// 3. Definimos todos os estilos para limpar os erros de 'styles.X'
const styles = StyleSheet.create({
  container: { flex: 1, padding: 20, backgroundColor: '#f8fafc', paddingTop: 60 },
  header: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20 },
  titulo: { fontSize: 28, fontWeight: 'bold', color: '#1e293b' },
  centro: { flex: 1, justifyContent: 'center' },
  botaoAtualizar: { backgroundColor: '#007AFF', paddingHorizontal: 15, paddingVertical: 8, borderRadius: 8 },
  textoBotao: { color: '#fff', fontWeight: 'bold' },
  card: {
    backgroundColor: '#fff',
    padding: 16,
    borderRadius: 12,
    marginBottom: 12,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1
  },
  info: { flex: 1 },
  modelo: { fontSize: 18, fontWeight: 'bold', color: '#334155', marginBottom: 4 },
  detalhe: { fontSize: 14, color: '#64748b' },
  badge: { paddingHorizontal: 10, paddingVertical: 4, borderRadius: 20 },
  vazio: { textAlign: 'center', marginTop: 50, color: '#94a3b8' }
});