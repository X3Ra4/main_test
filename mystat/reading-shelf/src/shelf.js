import React, { createContext, useContext, useEffect, useRef, useState } from "react";
import AsyncStorage from "@react-native-async-storage/async-storage";

const key = "reading-shelf-v1";
const initial = { books: {}, name: "" };
const Context = createContext(null);
export const statuses = { planned: "Хочу прочитати", reading: "Читаю", finished: "Прочитано" };

export function ShelfProvider({ children }) {
  const [state, setState] = useState(initial);
  const stateRef = useRef(initial);
  const queue = useRef(Promise.resolve());
  const [ready, setReady] = useState(false);
  const [error, setError] = useState("");

  async function restore() {
    setError("");
    try {
      const raw = await AsyncStorage.getItem(key);
      stateRef.current = raw ? JSON.parse(raw) : initial;
      setState(stateRef.current);
      setReady(true);
    } catch {
      setError("Не вдалося відкрити локальні дані.");
    }
  }

  useEffect(() => { void restore(); }, []);

  function update(change) {
    const operation = queue.current.then(async () => {
      const next = change(stateRef.current);
      await AsyncStorage.setItem(key, JSON.stringify(next));
      stateRef.current = next;
      setState(next);
      setError("");
    });
    queue.current = operation.catch(() => { setError("Не вдалося зберегти зміни. Спробуйте ще раз."); });
    return operation.then(() => true, () => false);
  }

  function saveBook(book) {
    return update(previous => ({ ...previous, books: { ...previous.books, [book.id]: book } }));
  }

  function removeBook(id) {
    return update(previous => {
      const books = { ...previous.books };
      delete books[id];
      return { ...previous, books };
    });
  }

  return <Context.Provider value={{
    ...state, ready, error, restore, saveBook, removeBook,
    saveName: name => update(previous => ({ ...previous, name })),
  }}>{children}</Context.Provider>;
}

export function useShelf() { return useContext(Context); }
