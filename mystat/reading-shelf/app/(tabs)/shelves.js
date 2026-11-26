import React, { useState } from "react";
import { FlatList, LayoutAnimation, Platform, Text, UIManager, View } from "react-native";
import { useRouter } from "expo-router";
import { statuses, useShelf } from "../../src/shelf";
import { BookRow, Button, Fade, Loading, styles } from "../../src/ui";

if (Platform.OS === "android") UIManager.setLayoutAnimationEnabledExperimental?.(true);

export default function Shelves() {
  const router = useRouter();
  const { books, ready, error, restore } = useShelf();
  const [filter, setFilter] = useState("all");
  const items = Object.values(books).filter(book => filter === "all" || book.status === filter);
  return <View style={styles.screen}><View style={styles.body}>
    <Text style={styles.title}>Мої полиці</Text>
    <View style={styles.row}>
      {Object.entries({ all: "Усі", ...statuses }).map(([key, label]) => <Button key={key} title={label}
        muted={filter !== key} onPress={() => {
          if (Platform.OS !== "web") LayoutAnimation.configureNext(LayoutAnimation.Presets.easeInEaseOut);
          setFilter(key);
        }} />)}
    </View>
    {!ready && (error ? <Button title="Повторити" onPress={restore} /> : <Loading />)}
    <FlatList data={items} keyExtractor={book => book.id}
      ListEmptyComponent={ready ? <Text style={styles.sub}>На цій полиці поки порожньо.</Text> : null}
      renderItem={({ item }) => <Fade><BookRow book={item}
        detail={statuses[item.status] + " · сторінка " + item.progress}
        onPress={() => router.push({ pathname: "/book/[id]", params: { id: item.id } })} /></Fade>} />
  </View></View>;
}
