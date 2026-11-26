import React, { useEffect, useRef, useState } from "react";
import { Animated, Text, TextInput, View } from "react-native";
import { useRouter } from "expo-router";
import { useShelf } from "../../src/shelf";
import { Button, Loading, styles } from "../../src/ui";

export default function Profile() {
  const router = useRouter();
  const { ready, name, books, saveName, error, restore } = useShelf();
  const [draft, setDraft] = useState("");
  const [invalid, setInvalid] = useState(false);
  const progress = useRef(new Animated.Value(0)).current;
  const total = Object.keys(books).length;
  const finished = Object.values(books).filter(book => book.status === "finished").length;
  const ratio = total ? finished / total : 0;

  useEffect(() => { setDraft(name); }, [name]);
  useEffect(() => {
    Animated.timing(progress, { toValue: ratio, duration: 360, useNativeDriver: false }).start();
  }, [progress, ratio]);

  if (!ready) return <View style={styles.body}>{error ?
    <Button title="Повторити" onPress={restore} /> : <Loading />}</View>;

  return <View style={styles.screen}><View style={styles.body}>
    <Text style={styles.title}>Профіль читача</Text>
    <TextInput style={styles.input} value={draft} onChangeText={setDraft} maxLength={50}
      placeholder="Як до вас звертатися?" />
    {invalid && <Text style={styles.error}>Ім’я має містити щонайменше два символи.</Text>}
    {!!error && <Text style={styles.error}>{error}</Text>}
    <Button title="Зберегти ім’я" onPress={async () => {
      const trimmed = draft.trim();
      setInvalid(trimmed.length < 2);
      if (trimmed.length >= 2 && await saveName(trimmed)) router.replace("/shelves");
    }} />
    <Text style={styles.sub}>Прочитано {finished} з {total} збережених книжок</Text>
    <View style={{ backgroundColor: "#dbe9d9", height: 12, borderRadius: 6, overflow: "hidden" }}>
      <Animated.View style={{ backgroundColor: "#156d55", height: 12,
        width: progress.interpolate({ inputRange: [0, 1], outputRange: ["0%", "100%"] }) }} />
    </View>
  </View></View>;
}
