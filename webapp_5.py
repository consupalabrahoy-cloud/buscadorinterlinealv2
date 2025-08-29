import streamlit as st
import re

def find_and_display_occurrences(lines, search_term):
    """
    Encuentra y muestra todas las ocurrencias de una subcadena en las líneas de texto,
    incluyendo la línea anterior (español) y la línea actual (griego),
    y además el encabezado de la sección y el número de versículo.
    """
    occurrences = []
    found_words = set()
    current_heading = "Sin encabezado"
    
    # Itera sobre las líneas con su índice
    for i, line in enumerate(lines):
        # 1. Identifica los encabezados de sección
        if re.match(r'^[^\d]+\s\d+$', line.strip()):
            current_heading = line.strip()
            continue # Salta a la siguiente línea, ya que esta es un encabezado
            
        # 2. Extrae el número de versículo y la línea en español
        spanish_line_match = re.match(r'^(\d+)\s(.+)$', line.strip())
        
        # 3. Busca la palabra en la línea griega, que es la siguiente
        if i + 1 < len(lines):
            greek_line_raw = lines[i + 1].strip()
            
            # Utiliza una expresión regular para encontrar todas las palabras en la línea griega
            words_in_greek_line = re.findall(r'[\w’]+', greek_line_raw)
            
            for word in words_in_greek_line:
                if search_term.lower() in word.lower():
                    found_words.add(word)
                    
                    if spanish_line_match:
                        verse_number = spanish_line_match.group(1)
                        spanish_text = spanish_line_match.group(2)
                        
                        # Se ha quitado el número de versículo de la línea griega
                        # si ya está al principio de la línea
                        if greek_line_raw.startswith(verse_number):
                           greek_text = greek_line_raw[len(verse_number):].strip()
                        else:
                           greek_text = greek_line_raw
                        
                        # Agrega la ocurrencia a la lista
                        occurrences.append({
                            "heading": current_heading,
                            "verse": verse_number,
                            "spanish_text": spanish_text,
                            "greek_text": greek_text,
                            "found_word": word
                        })
    
    return sorted(list(found_words)), occurrences

def main():
    """
    Función principal de la aplicación Streamlit.
    Configura la interfaz y maneja la lógica.
    """
    st.title("Buscador avanzado en texto interlineal español-griego")
    st.markdown("---")
    
    st.write("Esta aplicación te ayuda a buscar palabras griegas en un archivo de texto interlineal (griego/español) y muestra las ocurrencias, incluyendo el encabezado y el versículo. 🔍")

    # Widget para la carga del archivo
    uploaded_file = st.file_uploader(
        "1. Sube tu archivo de texto (.txt) con interlineal español-griego:",
        type=['txt']
    )

    # Widget para la entrada de la subcadena a buscar
    search_term = st.text_input(
        "2. Ingresa la secuencia de letras a buscar en las palabras griegas:",
        placeholder="Ejemplo: σπ"
    )

    st.markdown("---")
    
    if st.button("3. Buscar y analizar"):
        if uploaded_file is None:
            st.warning("Por favor, sube un archivo de texto para analizar.")
        elif not search_term:
            st.warning("Por favor, ingresa una secuencia de letras a buscar.")
        else:
            try:
                # Lee el contenido del archivo y lo divide en líneas
                file_content = uploaded_file.read().decode("utf-8")
                lines = file_content.splitlines()

                # Elimina las líneas vacías para un mejor procesamiento
                lines = [line for line in lines if line.strip()]

                # Llama a la función principal para buscar y obtener las ocurrencias
                unique_words, all_occurrences = find_and_display_occurrences(lines, search_term)

                # Muestra la lista de palabras únicas encontradas
                if unique_words:
                    st.subheader(f"Palabras únicas encontradas ({len(unique_words)}):")
                    st.write(", ".join(unique_words))
                    
                    st.markdown("---")
                    
                    # Muestra el contexto de cada ocurrencia
                    st.subheader("Ocurrencias y su contexto:")
                    for occurrence in all_occurrences:
                        # Muestra el encabezado
                        st.markdown(f"**{occurrence['heading']}**")
                        # Muestra el versículo y la línea en español
                        st.markdown(f"{occurrence['verse']} {occurrence['spanish_text']}")
                        # Muestra el versículo y la línea en griego
                        st.markdown(f"{occurrence['verse']} {occurrence['greek_text']}")
                        # Muestra la palabra encontrada
                        st.markdown(f"**Palabra encontrada:** `{occurrence['found_word']}`")
                        st.markdown("---")
                else:
                    st.warning(f"No se encontraron palabras que contengan '{search_term}' en el archivo.")

            except Exception as e:
                st.error(f"Ocurrió un error al procesar el archivo: {e}")

# Ejecuta la función principal si el script se ejecuta directamente
if __name__ == "__main__":
    main()



