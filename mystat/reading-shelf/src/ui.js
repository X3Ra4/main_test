import React, { useEffect, useRef } from "react";
import { ActivityIndicator, Animated, Image, Pressable, StyleSheet, Text, View } from "react-native";
import { coverUrl } from "./library";

export function Button({ title, onPress, muted = false, disabled = false }) {
  const scale = useRef(new Animated.Value(1)).current;
  const animate = value => Animated.spring(scale, { toValue: value, speed: 24, useNativeDriver: true }).start();
  return <Animated.View style={{ transform: [{ scale }] }}>
    <Pressable accessibilityRole="button" disabled={disabled} onPress={onPress}
      onPressIn={() => animate(0.96)} onPressOut={() => animate(1)}
      style={[styles.button, muted && styles.muted, disabled && { opacity: 0.55 }]}>
      <Text style={muted ? styles.mutedText : styles.buttonText}>{title}</Text>
    </Pressable>
  </Animated.View>;
}

export function Fade({ children }) {
  const opacity = useRef(new Animated.Value(0)).current;
  useEffect(() => {
    const animation = Animated.timing(opacity, { toValue: 1, duration: 260, useNativeDriver: true });
    animation.start();
    return () => animation.stop();
  }, [opacity]);
  return <Animated.View style={{ opacity }}>{children}</Animated.View>;
}

export function Loading() {
  return <View style={styles.center}><ActivityIndicator color="#156d55" size="large" />
    <Text style={styles.sub}>Завантаження…</Text></View>;
}

export function Cover({ book, large = false }) {
  const style = large ? styles.largeCover : styles.cover;
  return book.cover ? <Image style={style} source={{ uri: coverUrl(book.cover) }} accessibilityLabel={book.title} />
    : <View style={[style, styles.center]}><Text style={styles.sub}>📖</Text></View>;
}

export function BookRow({ book, onPress, detail }) {
  return <Pressable accessibilityRole="button" style={styles.card} onPress={onPress}>
    <Cover book={book} />
    <View style={{ flex: 1, gap: 4 }}>
      <Text style={styles.bookTitle}>{book.title}</Text>
      {!!book.authors && <Text style={styles.sub}>{book.authors}</Text>}
      {!!detail && <Text style={styles.sub}>{detail}</Text>}
    </View>
  </Pressable>;
}

export const styles = StyleSheet.create({
  screen: { flex: 1, backgroundColor: "#f4f1e8" },
  body: { flex: 1, width: "100%", maxWidth: 760, alignSelf: "center", paddingHorizontal: 20, paddingTop: 18, gap: 12 },
  content: { width: "100%", maxWidth: 760, alignSelf: "center", padding: 20, gap: 12 },
  title: { fontSize: 32, color: "#13352f", fontWeight: "800" },
  bookTitle: { fontSize: 17, color: "#163c34", fontWeight: "700" },
  sub: { color: "#4f665f", lineHeight: 21 },
  error: { color: "#963a43", paddingVertical: 6 },
  input: { borderWidth: 1, borderColor: "#c5d1c1", backgroundColor: "#fffef9", padding: 13, borderRadius: 12 },
  button: { backgroundColor: "#156d55", alignItems: "center", padding: 13, borderRadius: 12 },
  muted: { backgroundColor: "#dbe9d9" },
  buttonText: { color: "white", fontWeight: "700" },
  mutedText: { color: "#194b3e", fontWeight: "700" },
  center: { alignItems: "center", justifyContent: "center", padding: 12 },
  cover: { width: 54, height: 78, borderRadius: 7, backgroundColor: "#dbe9d9" },
  largeCover: { width: 125, height: 185, borderRadius: 9, backgroundColor: "#dbe9d9" },
  card: { flexDirection: "row", alignItems: "center", gap: 13, backgroundColor: "#fffef9", padding: 12, borderRadius: 14, marginBottom: 8 },
  row: { flexDirection: "row", flexWrap: "wrap", gap: 8 },
});
