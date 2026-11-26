import React from "react";
import { Tabs } from "expo-router";

export default function Layout() {
  return <Tabs screenOptions={{
    headerStyle: { backgroundColor: "#f4f1e8" },
    headerTintColor: "#13352f",
    tabBarActiveTintColor: "#156d55",
    tabBarInactiveTintColor: "#53665e",
  }}>
    <Tabs.Screen name="index" options={{ title: "Пошук" }} />
    <Tabs.Screen name="shelves" options={{ title: "Мої полиці" }} />
    <Tabs.Screen name="profile" options={{ title: "Профіль" }} />
  </Tabs>;
}
