import React from "react";
import { Stack } from "expo-router";
import { ShelfProvider } from "../src/shelf";

export default function Layout() {
  return <ShelfProvider>
    <Stack screenOptions={{ headerTintColor: "#13352f", headerStyle: { backgroundColor: "#f4f1e8" } }}>
      <Stack.Screen name="(tabs)" options={{ headerShown: false }} />
      <Stack.Screen name="book/[id]" options={{ title: "Книжка" }} />
    </Stack>
  </ShelfProvider>;
}
