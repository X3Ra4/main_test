import React, { useEffect, useState } from "react";
import { FlatList, Pressable, SafeAreaView, StyleSheet, Text, TextInput, View } from "react-native";
import AsyncStorage from "@react-native-async-storage/async-storage";
import * as Crypto from "expo-crypto";

const key = "mystat.local-todo.v1";
const empty = { accounts: {}, active: null };
const digest = (password, salt) => Crypto.digestStringAsync(Crypto.CryptoDigestAlgorithm.SHA256, salt + password);

function Button({ label, onPress, light = false }) {
  return <Pressable accessibilityRole="button" onPress={onPress} style={[styles.button, light && styles.light]}>
    <Text style={[styles.buttonText, light && styles.lightText]}>{label}</Text>
  </Pressable>;
}

export default function App() {
  const [data, setData] = useState(empty);
  const [ready, setReady] = useState(false);
  const [busy, setBusy] = useState(false);
  const [register, setRegister] = useState(false);
  const [name, setName] = useState("");
  const [password, setPassword] = useState("");
  const [task, setTask] = useState("");
  const [editing, setEditing] = useState(null);
  const [error, setError] = useState("");

  async function read() {
    try {
      const saved = await AsyncStorage.getItem(key);
      setData(saved ? JSON.parse(saved) : empty);
      setError("");
      setReady(true);
    } catch {
      setError("Не вдалося прочитати локальне сховище.");
    }
  }

  useEffect(() => { void read(); }, []);

  async function persist(next) {
    try {
      await AsyncStorage.setItem(key, JSON.stringify(next));
      setData(next);
      setError("");
      return true;
    } catch {
      setError("Не вдалося зберегти зміни. Спробуйте ще раз.");
      return false;
    }
  }

  const current = data.active ? data.accounts[data.active] : null;

  async function authenticate() {
    if (busy) return;
    const id = name.trim().toLowerCase();
    if (!/^[a-z0-9_]{3,32}$/.test(id) || password.length < 6) {
      setError("Логін: 3–32 латинські символи, цифри або _. Пароль: від 6 символів.");
      return;
    }
    setBusy(true);
    try {
      const existing = Object.hasOwn(data.accounts, id) ? data.accounts[id] : null;
      if (register && existing) { setError("Цей логін уже існує."); return; }
      if (!register && (!existing || await digest(password, existing.salt) !== existing.hash)) {
        setError("Невірний логін або пароль.");
        return;
      }
      const salt = register ? Crypto.randomUUID() : null;
      const account = register ? { salt, hash: await digest(password, salt), tasks: [] } : existing;
      if (await persist({ accounts: { ...data.accounts, [id]: account }, active: id })) setPassword("");
    } catch {
      setError("Не вдалося виконати вхід. Спробуйте ще раз.");
    } finally {
      setBusy(false);
    }
  }

  async function saveTasks(tasks) {
    if (busy) return false;
    setBusy(true);
    try {
      return await persist({ ...data, accounts: { ...data.accounts, [data.active]: { ...current, tasks } } });
    } finally {
      setBusy(false);
    }
  }

  async function saveTask() {
    const title = task.trim();
    if (!title) { setError("Введіть назву завдання."); return; }
    const tasks = editing
      ? current.tasks.map(item => item.id === editing ? { ...item, title } : item)
      : [{ id: Crypto.randomUUID(), title, done: false }, ...current.tasks];
    if (await saveTasks(tasks)) { setTask(""); setEditing(null); }
  }

  return <SafeAreaView style={styles.screen}>
    <View style={styles.body}>
      <Text style={styles.title}>{current ? "Мої завдання" : "План на день"}</Text>
      {!ready && <Button label={error ? "Повторити" : "Завантаження…"} onPress={read} />}
      {ready && !current && <>
        <Text style={styles.subtitle}>{register ? "Створіть локальний акаунт" : "Увійдіть до свого списку"}</Text>
        <TextInput style={styles.input} value={name} onChangeText={setName} placeholder="Логін" autoCapitalize="none" />
        <TextInput style={styles.input} value={password} onChangeText={setPassword} placeholder="Пароль" secureTextEntry />
        <Button label={busy ? "Зачекайте…" : register ? "Створити акаунт" : "Увійти"} onPress={authenticate} />
        <Button light label={register ? "Уже є акаунт" : "Зареєструватися"} onPress={() => {
          if (!busy) { setRegister(!register); setError(""); }
        }} />
      </>}
      {current && <>
        <Text style={styles.subtitle}>{data.active} · {current.tasks.filter(item => item.done).length} виконано</Text>
        <Button light label="Вийти" onPress={async () => {
          if (!busy && await persist({ ...data, active: null })) { setTask(""); setEditing(null); setRegister(false); }
        }} />
        <TextInput style={styles.input} value={task} onChangeText={setTask} placeholder="Наприклад, повторити Python" maxLength={120} />
        <Button label={editing ? "Зберегти зміни" : "Додати завдання"} onPress={saveTask} />
        {editing && <Button light label="Скасувати редагування" onPress={() => { setEditing(null); setTask(""); }} />}
        <FlatList data={current.tasks} keyExtractor={item => item.id}
          ListEmptyComponent={<Text style={styles.subtitle}>Завдань поки немає.</Text>}
          renderItem={({ item }) => <View style={styles.row}>
            <Pressable style={styles.task} onPress={() => saveTasks(current.tasks.map(previous =>
              previous.id === item.id ? { ...previous, done: !previous.done } : previous))}>
              <Text style={item.done && styles.done}>{item.done ? "✓" : "○"} {item.title}</Text>
            </Pressable>
            <Pressable onPress={() => { setTask(item.title); setEditing(item.id); }}><Text style={styles.link}>Змінити</Text></Pressable>
            <Pressable onPress={async () => {
              if (await saveTasks(current.tasks.filter(previous => previous.id !== item.id)) && editing === item.id) {
                setEditing(null); setTask("");
              }
            }}><Text style={styles.link}>Видалити</Text></Pressable>
          </View>}
        />
      </>}
      {!!error && <Text accessibilityRole="alert" style={styles.error}>{error}</Text>}
    </View>
  </SafeAreaView>;
}

const styles = StyleSheet.create({
  screen: { flex: 1, backgroundColor: "#eef0fa" },
  body: { flex: 1, width: "100%", maxWidth: 600, alignSelf: "center", padding: 24, paddingTop: 44, gap: 10 },
  title: { fontSize: 34, fontWeight: "800", color: "#27195b" },
  subtitle: { color: "#4a4271", paddingVertical: 6 },
  input: { padding: 14, backgroundColor: "white", borderRadius: 14, borderColor: "#dcd6ed", borderWidth: 1 },
  button: { padding: 14, backgroundColor: "#573fc2", borderRadius: 14, alignItems: "center" },
  light: { backgroundColor: "#e0d9f9" },
  buttonText: { color: "white", fontWeight: "700" },
  lightText: { color: "#382084" },
  row: { flexDirection: "row", flexWrap: "wrap", gap: 12, alignItems: "center", backgroundColor: "white", padding: 14, borderRadius: 14, marginBottom: 8 },
  task: { flex: 1, minWidth: 90 },
  done: { textDecorationLine: "line-through", color: "#5f557a" },
  link: { color: "#473394" },
  error: { color: "#a32130" },
});
