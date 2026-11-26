import React, { useState } from "react";
import { Alert, FlatList, Platform, Pressable, SafeAreaView, StyleSheet, Text, View } from "react-native";

const moods = ["😢", "😕", "😐", "🙂", "😄"];

function confirm(title, message, action) {
  if (Platform.OS === "web") {
    if (window.confirm(message)) action();
    return;
  }
  Alert.alert(title, message, [
    { text: "Скасувати", style: "cancel" },
    { text: "Видалити", style: "destructive", onPress: action },
  ]);
}

export default function App() {
  const [entries, setEntries] = useState([]);
  const counts = Object.fromEntries(moods.map(mood => [mood, 0]));
  entries.forEach(entry => { counts[entry.mood] += 1; });
  const best = Math.max(...Object.values(counts));

  function add(mood) {
    const now = new Date();
    const entry = { id: now.getTime() + "-" + Math.random().toString(36).slice(2), mood, now };
    setEntries(previous => [entry, ...previous]);
  }

  return (
    <SafeAreaView style={styles.screen}>
      <View style={styles.body}>
        <Text style={styles.title}>Трекер настрою</Text>
        <Text style={styles.summary}>
          {best ? "Найчастіше: " + moods.filter(mood => counts[mood] === best).join(" ") : "Як ви почуваєтеся?"}
        </Text>
        <View style={styles.moods}>
          {moods.map(mood => (
            <Pressable key={mood} accessibilityRole="button" accessibilityLabel={"Додати " + mood} onPress={() => add(mood)}>
              <Text style={styles.emoji}>{mood}</Text>
            </Pressable>
          ))}
        </View>
        <FlatList data={entries} keyExtractor={entry => entry.id}
          ListEmptyComponent={<Text style={styles.empty}>Історія поки порожня.</Text>}
          renderItem={({ item }) => (
            <Pressable style={styles.row} onPress={() => confirm("Видалити запис", "Видалити цей запис?",
              () => setEntries(previous => previous.filter(entry => entry.id !== item.id)))}>
              <Text style={styles.emoji}>{item.mood}</Text>
              <Text>{item.now.toLocaleString("uk-UA")}</Text>
            </Pressable>
          )}
        />
        {entries.length > 0 && <Pressable onPress={() => confirm("Очистити історію",
          "Видалити всі записи історії?", () => setEntries([]))}>
          <Text style={styles.clear}>Очистити всю історію</Text>
        </Pressable>}
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  screen: { flex: 1, backgroundColor: "#ecf4ed" },
  body: { width: "100%", maxWidth: 540, alignSelf: "center", flex: 1, padding: 22, paddingTop: 48 },
  title: { fontSize: 32, fontWeight: "800", color: "#153b32" },
  summary: { marginTop: 10, color: "#38574f", fontSize: 17 },
  moods: { flexDirection: "row", justifyContent: "space-around", backgroundColor: "white", borderRadius: 18, padding: 12, marginVertical: 18 },
  emoji: { fontSize: 28 },
  row: { flexDirection: "row", gap: 14, alignItems: "center", backgroundColor: "white", padding: 14, borderRadius: 14, marginBottom: 8 },
  empty: { textAlign: "center", padding: 20, color: "#38574f" },
  clear: { color: "#a02035", textAlign: "center", padding: 14, fontWeight: "700" },
});
