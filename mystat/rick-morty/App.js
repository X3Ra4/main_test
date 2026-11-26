import React, { useEffect, useRef, useState } from "react";
import { ActivityIndicator, Animated, FlatList, Image, Pressable, SafeAreaView, ScrollView, StyleSheet, Text, TextInput, View } from "react-native";

const endpoint = "https://rickandmortyapi.com/api/character/";
const emptyFilters = { status: "", species: "", gender: "" };
const filterOptions = {
  status: [["", "Будь-який"], ["alive", "Живий"], ["dead", "Мертвий"], ["unknown", "Невідомо"]],
  gender: [["", "Будь-яка"], ["female", "Жіноча"], ["male", "Чоловіча"], ["genderless", "Без статі"], ["unknown", "Невідомо"]],
};

async function page(filters, number, signal) {
  const search = new URLSearchParams({ page: String(number) });
  Object.entries(filters).forEach(([key, value]) => { if (value.trim()) search.set(key, value.trim()); });
  const response = await fetch(endpoint + "?" + search.toString(), { signal });
  if (response.status === 404) return null;
  if (!response.ok) throw new Error("Помилка API");
  return response.json();
}

export default function App() {
  const [draft, setDraft] = useState(emptyFilters);
  const [filters, setFilters] = useState(emptyFilters);
  const [request, setRequest] = useState(0);
  const [character, setCharacter] = useState(null);
  const [history, setHistory] = useState([]);
  const [stats, setStats] = useState({ total: 0, Alive: 0, Dead: 0, unknown: 0 });
  const [state, setState] = useState("loading");
  const fade = useRef(new Animated.Value(0)).current;
  const spring = useRef(new Animated.Value(1)).current;

  function reveal(item) {
    setCharacter(item);
    fade.setValue(0);
    Animated.timing(fade, { toValue: 1, duration: 320, useNativeDriver: true }).start();
  }

  useEffect(() => {
    const controller = new AbortController();
    async function load() {
      setState("loading");
      try {
        const first = await page(filters, 1, controller.signal);
        if (controller.signal.aborted) return;
        if (!first?.info.count) { setState("empty"); setCharacter(null); return; }
        const index = Math.floor(Math.random() * first.info.count);
        const number = Math.floor(index / 20) + 1;
        const result = number === 1 ? first : await page(filters, number, controller.signal);
        if (controller.signal.aborted) return;
        const item = result?.results[index % 20];
        if (!item) { setState("empty"); setCharacter(null); return; }
        reveal(item);
        setHistory(previous => [item, ...previous.filter(entry => entry.id !== item.id)].slice(0, 8));
        setStats(previous => ({ ...previous, total: previous.total + 1, [item.status]: (previous[item.status] || 0) + 1 }));
        setState("success");
      } catch {
        if (!controller.signal.aborted) setState("error");
      }
    }
    void load();
    return () => controller.abort();
  }, [filters, request]);

  function next() {
    spring.setValue(0.88);
    Animated.spring(spring, { toValue: 1, friction: 3, useNativeDriver: true }).start();
    setRequest(value => value + 1);
  }

  return <SafeAreaView style={styles.screen}>
    <ScrollView contentContainerStyle={styles.body}>
      <Text style={styles.title}>Рік та Морті</Text>
      <Text style={styles.sub}>Випадковий персонаж</Text>
      {Object.entries(filterOptions).map(([key, options]) => (
        <View style={styles.options} key={key}>
          <Text style={styles.sub}>{key === "status" ? "Статус" : "Стать"} </Text>
          {options.map(([value, label]) => <Pressable key={value} onPress={() => setDraft({ ...draft, [key]: value })}>
            <Text style={[styles.chip, draft[key] === value && styles.chipActive]}>{label}</Text>
          </Pressable>)}
        </View>
      ))}
      <TextInput value={draft.species} onChangeText={species => setDraft({ ...draft, species })}
        placeholder="Вид, наприклад Human" placeholderTextColor="#a3b9b7" style={styles.input} />
      <View style={styles.options}>
        <Pressable onPress={() => setFilters({ ...draft })}><Text style={styles.chip}>Застосувати</Text></Pressable>
        <Pressable onPress={() => { setDraft({ ...emptyFilters }); setFilters({ ...emptyFilters }); }}>
          <Text style={styles.chip}>Очистити</Text>
        </Pressable>
      </View>
      {state === "loading" && <ActivityIndicator color="#d8f56d" size="large" />}
      {state === "error" && <Text style={styles.sub}>Не вдалося отримати дані. Натисніть «Далі», щоб повторити.</Text>}
      {state === "empty" && <Text style={styles.sub}>За цими фільтрами персонажів немає.</Text>}
      {state === "success" && character && <Animated.View style={[styles.card, { opacity: fade,
        transform: [{ translateY: fade.interpolate({ inputRange: [0, 1], outputRange: [16, 0] }) }] }]}>
        <Image source={{ uri: character.image }} style={styles.image} accessibilityLabel={character.name} />
        <Text style={styles.name}>{character.name}</Text>
        <Text style={styles.sub}>{character.status} · {character.species} · {character.gender}</Text>
      </Animated.View>}
      <Animated.View style={{ transform: [{ scale: spring }] }}>
        <Pressable onPress={next} style={styles.button}><Text style={styles.buttonText}>Далі</Text></Pressable>
      </Animated.View>
      <Text style={styles.sub}>Переглянуто {stats.total} · живих {stats.Alive} · мертвих {stats.Dead}</Text>
      {history.length > 0 && <FlatList horizontal data={history} keyExtractor={item => String(item.id)}
        renderItem={({ item }) => <Pressable onPress={() => { setState("success"); reveal(item); }}>
          <Image source={{ uri: item.image }} style={styles.thumb} accessibilityLabel={item.name} />
        </Pressable>} />}
    </ScrollView>
  </SafeAreaView>;
}

const styles = StyleSheet.create({
  screen: { flex: 1, backgroundColor: "#10221f" },
  body: { width: "100%", maxWidth: 550, alignSelf: "center", padding: 22, paddingTop: 42, gap: 12 },
  title: { fontSize: 34, fontWeight: "800", color: "#dbf779" },
  sub: { color: "#c8dcda", fontSize: 15 },
  options: { flexDirection: "row", flexWrap: "wrap", gap: 7, alignItems: "center" },
  chip: { backgroundColor: "#28403c", color: "#e6f3e5", padding: 8, borderRadius: 10 },
  chipActive: { backgroundColor: "#597344" },
  input: { color: "white", padding: 11, borderColor: "#64817c", borderWidth: 1, borderRadius: 10 },
  card: { backgroundColor: "#213733", borderRadius: 19, padding: 14, gap: 8 },
  image: { width: "100%", aspectRatio: 1.3, borderRadius: 12, maxHeight: 320 },
  name: { color: "white", fontSize: 25, fontWeight: "700" },
  button: { backgroundColor: "#d8f56d", alignItems: "center", padding: 15, borderRadius: 14 },
  buttonText: { color: "#16271d", fontSize: 16, fontWeight: "800" },
  thumb: { width: 62, height: 62, borderRadius: 10, marginRight: 8 },
});
