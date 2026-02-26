import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet, Alert, ScrollView } from 'react-native';

export default function CadastroScreen() {
  const [modelo, setModelo] = useState('');
  const [imei, setImei] = useState('');
  const [serie, setSerie] = useState('');
  const [status, setStatus] = useState('Disponível');

  const salvar = async () => {
    if (!modelo || !imei || !serie) {
      Alert.alert("Erro", "Por favor, preencha todos os campos.");
      return;
    }

    try {
      const response = await fetch('http://10.0.2.2:5000/aparelhos', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          modelo: modelo,
          imei: imei,
          numero_serie: serie,
          status: status
        })
      });

      if (response.ok) {
        Alert.alert("Sucesso", "Aparelho cadastrado!");
        setModelo(''); setImei(''); setSerie(''); // Limpa o formulário
      }
    } catch (error) {
      Alert.alert("Erro", "Não foi possível conectar ao servidor.");
    }
  };

  return (
    <ScrollView style={styles.container}>
      <Text style={styles.titulo}>Novo Aparelho</Text>

      <Text style={styles.label}>Modelo</Text>
      <TextInput style={styles.input} value={modelo} onChangeText={setModelo} placeholder="Ex: Samsung S23" />

      <Text style={styles.label}>IMEI</Text>
      <TextInput style={styles.input} value={imei} onChangeText={setImei} keyboardType="numeric" placeholder="15 dígitos" />

      <Text style={styles.label}>Número de Série</Text>
      <TextInput style={styles.input} value={serie} onChangeText={setSerie} placeholder="S/N do fabricante" />

      <TouchableOpacity style={styles.botao} onPress={salvar}>
        <Text style={styles.textoBotao}>Salvar Aparelho</Text>
      </TouchableOpacity>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20, backgroundColor: '#fff', paddingTop: 60 },
  titulo: { fontSize: 26, fontWeight: 'bold', marginBottom: 30 },
  label: { fontSize: 16, marginBottom: 5, color: '#333' },
  input: { borderWidth: 1, borderColor: '#ddd', padding: 12, borderRadius: 8, marginBottom: 20, fontSize: 16 },
  botao: { backgroundColor: '#28a745', padding: 15, borderRadius: 10, alignItems: 'center' },
  textoBotao: { color: '#fff', fontSize: 18, fontWeight: 'bold' }
});