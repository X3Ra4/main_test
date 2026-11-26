import React, { useEffect, useState } from "react";
import { ScrollView, Text, TextInput, View } from "react-native";
import { useLocalSearchParams, useRouter } from "expo-router";
import { getBook } from "../../src/library";
import { statuses, useShelf } from "../../src/shelf";
import { Button, Cover, Fade, Loading, styles } from "../../src/ui";

export default function Book() {
  const router = useRouter();
  const { id } = useLocalSearchParams();
  const { books, ready, saveBook, removeBook, error, restore } = useShelf();
  const saved = books[id];
  const [book, setBook] = useState(null);
  const [state, setState] = useState("loading");
  const [attempt, setAttempt] = useState(0);
  const [status, setStatus] = useState("planned");
  const [progress, setProgress] = useState("0");
  const [notes, setNotes] = useState("");
  const [invalid, setInvalid] = useState(false);

  useEffect(() => {
    setStatus(saved?.status ?? "planned");
    setProgress(String(saved?.progress ?? 0));
    setNotes(saved?.notes ?? "");
  }, [saved]);

  useEffect(() => {
    const request = new AbortController();
    setState("loading");
    setBook(null);
    getBook(id, request.signal).then(result => {
      if (request.signal.aborted) return;
      setBook(result);
      setState(result ? "ready" : "empty");
    }).catch(() => {
      if (!request.signal.aborted) setState("error");
    });
    return () => request.abort();
  }, [id, attempt]);

  const current = book ?? saved;

  return <ScrollView style={styles.screen} contentContainerStyle={styles.content}>
    {state === "loading" && !current && <Loading />}
    {state === "error" && <>
      <Text style={styles.error}>Не вдалося завантажити опис книжки.</Text>
      <Button title="Повторити" onPress={() => setAttempt(value => value + 1)} />
    </>}
    {state === "empty" && !current && <Text style={styles.sub}>Книжку не знайдено.</Text>}
    {!!current && <Fade key={current.id}>
      <View style={{ gap: 12 }}>
        <Cover book={current} large />
        <Text style={styles.title}>{current.title}</Text>
        <Text style={styles.sub}>{current.description ?? "Open Library не надала опису."}</Text>
        <View style={styles.row}>
          {Object.entries(statuses).map(([key, title]) => <Button key={key} title={title}
            muted={key !== status} onPress={() => setStatus(key)} />)}
        </View>
        <Text style={styles.sub}>Поточна сторінка</Text>
        <TextInput style={styles.input} value={progress} onChangeText={setProgress} keyboardType="number-pad" maxLength={6} />
        <TextInput style={styles.input} value={notes} onChangeText={setNotes} maxLength={2000}
          placeholder="Особисті нотатки" multiline />
        {invalid && <Text style={styles.error}>Введіть цілий номер сторінки від 0 до 999999.</Text>}
        {!!error && <Text style={styles.error}>{error}</Text>}
        {!ready && !!error && <Button title="Повторити відкриття локальних даних" onPress={restore} />}
        <Button title="Зберегти на полиці" disabled={!ready} onPress={async () => {
          const valid = /^\d{1,6}$/.test(progress);
          setInvalid(!valid);
          if (valid && await saveBook({ ...current, status, progress: Number(progress), notes: notes.trim() })) {
            router.replace("/shelves");
          }
        }} />
        {!!saved && <Button title="Прибрати з полиці" muted onPress={async () => {
          if (await removeBook(id)) router.replace("/shelves");
        }} />}
      </View>
    </Fade>}
  </ScrollView>;
}
