const origin = "https://openlibrary.org";

async function get(path, signal) {
  const response = await fetch(origin + path, { signal });
  if (response.status === 404) return null;
  if (!response.ok) throw new Error("Open Library недоступна");
  return response.json();
}

export async function searchBooks(query, page, signal) {
  const params = new URLSearchParams({
    q: query,
    page: String(page),
    limit: "20",
    fields: "key,title,author_name,cover_i,first_publish_year",
  });
  const result = await get("/search.json?" + params, signal);
  const books = (result?.docs ?? []).filter(item => /^\/works\/OL\d+W$/.test(item.key)).map(item => ({
    id: item.key.split("/").pop(),
    title: item.title,
    authors: item.author_name?.join(", "),
    cover: item.cover_i,
    year: item.first_publish_year,
  }));
  return { books, more: page * 20 < (result?.numFound ?? 0) };
}

export async function getBook(id, signal) {
  if (!/^OL\d+W$/.test(id)) return null;
  const data = await get("/works/" + id + ".json", signal);
  return data && {
    id,
    title: data.title,
    cover: data.covers?.find(id => id > 0),
    description: typeof data.description === "string" ? data.description : data.description?.value,
  };
}

export const coverUrl = id => "https://covers.openlibrary.org/b/id/" + id + "-M.jpg";
