import React, { useEffect, useState } from "react";
import { FlatList, Text, TextInput, View } from "react-native";
import { useRouter } from "expo-router";
import { searchBooks } from "../../src/library";
import { BookRow, Button, Fade, Loading, styles } from "../../src/ui";

export default function Search() {
  const router = useRouter();
  const [draft, setDraft] = useState("");
  const [query, setQuery] = useState("Hobbit");
  const [page, setPage] = useState(1);
  const [items, setItems] = useState([]);
  const [more, setMore] = useState(false);
  const [status, setStatus] = useState("loading");
  const [revision, setRevision] = useState(0);
  const [validation, setValidation] = useState("");

  function reload(nextQuery = query) {
    setQuery(nextQuery);
    setPage(1);
    setStatus("loading");
    setRevision(value => value + 1);
  }

  useEffect(() => {
    const request = new AbortController();
    searchBooks(query, page, request.signal).then(result => {
      if (request.signal.aborted) return;
      setMore(result.more);
      setItems(previous => page === 1 ? result.books :
        [...new Map([...previous, ...result.books].map(book => [book.id, book])).values()]);
      setStatus("ready");
    }).catch(() => {
      if (!request.signal.aborted) setStatus("error");
    });
    return () => request.abort();
  }, [query, page, revision]);

  function submit() {
    const value = draft.trim();
    if (value.length < 2) { setValidation("Введіть щонайменше два символи."); return; }
    setValidation("");
    setItems([]);
    reload(value);
  }

  return <View style={styles.screen}><View style={styles.body}>
    <Text style={styles.title}>Книжкова полиця</Text>
    <TextInput style={styles.input} value={draft} maxLength={100} onChangeText={setDraft} onSubmitEditing={submit}
      returnKeyType="search" placeholder="Назва книжки або автор" />
    <Button title="Знайти" onPress={submit} />
    {!!validation && <Text style={styles.error}>{validation}</Text>}
    <Text style={styles.sub}>Результати для «{query}»</Text>
    {status === "error" && <>
      <Text style={styles.error}>Не вдалося завантажити результати.</Text>
      <Button title="Повторити" onPress={() => {
        setStatus("loading");
        setRevision(value => value + 1);
      }} />
    </>}
    <FlatList data={items} keyExtractor={book => book.id}
      refreshing={status === "loading" && items.length > 0 && page === 1}
      onRefresh={() => reload()}
      ListEmptyComponent={status === "loading" ? <Loading /> : status === "ready" ?
        <Text style={styles.sub}>Книжок за цим запитом немає.</Text> : null}
      ListFooterComponent={items.length > 0 && more && status === "ready" ?
        <Button title="Більше результатів" onPress={() => { setStatus("loading"); setPage(value => value + 1); }} /> :
        items.length > 0 && status === "loading" && page > 1 ? <Loading /> : null}
      renderItem={({ item }) => <Fade><BookRow book={item} detail={item.year}
        onPress={() => router.push({ pathname: "/book/[id]", params: { id: item.id } })} /></Fade>} />
  </View></View>;
}
