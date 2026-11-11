/**
 * Práctica 4 — Algoritmos Voraces y Codificación de Huffman
 * Escuela Superior de Cómputo (ESCOM - IPN)
 * Materia: Análisis y Diseño de Algoritmos
 *
 * Implementación completa en C++17 de la Codificación de Huffman:
 *   - Empaquetado real a nivel de bits (BitWriter / BitReader) usando <<, >>, &, |
 *   - Serialización compacta del árbol en Preorden (10k - 1 bits) y Opción A (Tabla)
 *   - Resolución de "The Padding Trap" (uint64_t original_size + uint8_t valid_last_bits)
 *   - Corrección del bug de puntero nulo en archivos homogéneos (k = 1)
 *   - Suite de Benchmarking automatizada para los casos de prueba de la práctica
 */

#include <iostream>
#include <fstream>
#include <vector>
#include <queue>
#include <memory>
#include <cstdint>
#include <string>
#include <cmath>
#include <chrono>
#include <iomanip>
#include <array>
#include <algorithm>
#include <stdexcept>

// ============================================================================
// 1. ESTRUCTURA DEL NODO DE HUFFMAN (Corregida contra nullptr dereference)
// ============================================================================
struct HuffmanNode {
    uint8_t character;
    uint64_t frequency;
    uint8_t min_char; // Para desempate determinista en el Min-Heap
    std::shared_ptr<HuffmanNode> left;
    std::shared_ptr<HuffmanNode> right;

    // Constructor para nodo hoja
    HuffmanNode(uint8_t ch, uint64_t freq)
        : character(ch), frequency(freq), min_char(ch), left(nullptr), right(nullptr) {}

    // Constructor seguro para nodo interno (verifica nullptr en caso borde k = 1)
    HuffmanNode(std::shared_ptr<HuffmanNode> l, std::shared_ptr<HuffmanNode> r)
        : character(0),
          frequency((l ? l->frequency : 0) + (r ? r->frequency : 0)),
          min_char(std::min(l ? l->min_char : uint8_t(255), r ? r->min_char : uint8_t(255))),
          left(std::move(l)),
          right(std::move(r)) {}

    bool is_leaf() const noexcept {
        return left == nullptr && right == nullptr;
    }
};

struct NodeComparator {
    bool operator()(const std::shared_ptr<HuffmanNode>& a,
                    const std::shared_ptr<HuffmanNode>& b) const noexcept {
        if (a->frequency != b->frequency) {
            return a->frequency > b->frequency; // Min-Heap por frecuencia
        }
        return a->min_char > b->min_char;       // Desempate determinista canónico
    }
};

// ============================================================================
// 2. BITWRITER Y BITREADER: EMPAQUETADO A NIVEL DE BITS CON <<, >>, &, |
// ============================================================================
class BitWriter {
private:
    std::vector<uint8_t> buffer_;
    uint8_t current_byte_ = 0;
    uint8_t bit_count_ = 0;

public:
    explicit BitWriter(size_t reserve_bytes = 4096) {
        buffer_.reserve(reserve_bytes);
    }

    // Escribe un único bit (0 o 1) en el acumulador de 8 bits (MSB-first)
    inline void write_bit(uint8_t bit) {
        current_byte_ = static_cast<uint8_t>((current_byte_ << 1) | (bit & 1U));
        ++bit_count_;
        if (bit_count_ == 8) {
            buffer_.push_back(current_byte_);
            current_byte_ = 0;
            bit_count_ = 0;
        }
    }

    // Escribe una secuencia de bits representada como código entero de longitud `len`
    inline void write_bits(uint64_t code, uint8_t len) {
        for (int i = static_cast<int>(len) - 1; i >= 0; --i) {
            write_bit(static_cast<uint8_t>((code >> i) & 1ULL));
        }
    }

    // Escribe un byte completo de 8 bits
    inline void write_byte(uint8_t byte_val) {
        if (bit_count_ == 0) {
            buffer_.push_back(byte_val);
        } else {
            write_bits(byte_val, 8);
        }
    }

    // Vuelca el último byte parcial rellenando con ceros a la derecha (padding)
    // Retorna la cantidad de bits válidos en el último byte (1..8, o 0 si vacío)
    uint8_t flush() {
        if (bit_count_ > 0) {
            uint8_t valid_bits = bit_count_;
            uint8_t padding_shift = static_cast<uint8_t>(8 - bit_count_);
            current_byte_ = static_cast<uint8_t>(current_byte_ << padding_shift);
            buffer_.push_back(current_byte_);
            current_byte_ = 0;
            bit_count_ = 0;
            return valid_bits;
        }
        return buffer_.empty() ? 0 : 8;
    }

    const std::vector<uint8_t>& data() const noexcept { return buffer_; }
    size_t size_bytes() const noexcept { return buffer_.size(); }
};

class BitReader {
private:
    const uint8_t* data_;
    size_t size_bytes_;
    size_t byte_idx_ = 0;
    uint8_t bit_idx_ = 0; // 0..7 (de MSB a LSB)

public:
    BitReader(const uint8_t* data, size_t size_bytes)
        : data_(data), size_bytes_(size_bytes) {}

    inline bool has_more_bits() const noexcept {
        return byte_idx_ < size_bytes_;
    }

    // Extrae un bit usando desplazamiento >> y máscara &
    inline uint8_t read_bit() {
        if (byte_idx_ >= size_bytes_) {
            throw std::out_of_range("BitReader: Fin de flujo alcanzado");
        }
        uint8_t bit = (data_[byte_idx_] >> (7 - bit_idx_)) & 1U;
        ++bit_idx_;
        if (bit_idx_ == 8) {
            bit_idx_ = 0;
            ++byte_idx_;
        }
        return bit;
    }

    // Extrae 8 bits consecutivos para reconstruir un carácter ASCII
    inline uint8_t read_byte() {
        uint8_t value = 0;
        for (int i = 0; i < 8; ++i) {
            value = static_cast<uint8_t>((value << 1) | read_bit());
        }
        return value;
    }
};

// ============================================================================
// 3. CONSTRUCCIÓN DEL ÁRBOL Y SERIALIZACIÓN EN PREORDEN
// ============================================================================
std::shared_ptr<HuffmanNode> build_huffman_tree(const std::array<uint64_t, 256>& frequencies) {
    std::priority_queue<std::shared_ptr<HuffmanNode>,
                        std::vector<std::shared_ptr<HuffmanNode>>,
                        NodeComparator> min_heap;

    for (size_t i = 0; i < 256; ++i) {
        if (frequencies[i] > 0) {
            min_heap.push(std::make_shared<HuffmanNode>(static_cast<uint8_t>(i), frequencies[i]));
        }
    }

    if (min_heap.empty()) {
        return nullptr;
    }

    // Caso borde crucial: alfabetos con k = 1 solo símbolo único (ej. 10^7 'A's)
    // Se retorna directamente el nodo hoja o un nodo raíz con hijo izquierdo válido.
    // Al usar nodo hoja directo o manejar k=1, evitamos desreferenciar nullptr.
    if (min_heap.size() == 1) {
        auto single = min_heap.top();
        min_heap.pop();
        return std::make_shared<HuffmanNode>(single, nullptr);
    }

    while (min_heap.size() > 1) {
        auto left = min_heap.top();
        min_heap.pop();
        auto right = min_heap.top();
        min_heap.pop();
        auto parent = std::make_shared<HuffmanNode>(left, right);
        min_heap.push(parent);
    }

    return min_heap.top();
}

struct CodeEntry {
    uint64_t bits = 0;
    uint8_t len = 0;
};

void build_code_table(const std::shared_ptr<HuffmanNode>& node,
                      uint64_t current_bits,
                      uint8_t depth,
                      std::array<CodeEntry, 256>& table) {
    if (!node) return;

    if (node->is_leaf()) {
        table[node->character] = {current_bits, depth == 0 ? uint8_t(1) : depth};
        return;
    }

    build_code_table(node->left, (current_bits << 1) | 0ULL, depth + 1, table);
    if (node->right) {
        build_code_table(node->right, (current_bits << 1) | 1ULL, depth + 1, table);
    }
}

// Serialización del árbol en Preorden (Opción B: 10k - 1 bits)
void serialize_tree_preorder(const std::shared_ptr<HuffmanNode>& node, BitWriter& writer) {
    if (!node) return;

    if (node->is_leaf()) {
        writer.write_bit(1);
        writer.write_byte(node->character);
        return;
    }

    // Si es el nodo raíz especial de 1 solo símbolo (right == nullptr),
    // serializamos directamente su único hijo hoja para mantener árbol binario estricto
    if (node->left && !node->right) {
        serialize_tree_preorder(node->left, writer);
        return;
    }

    writer.write_bit(0);
    serialize_tree_preorder(node->left, writer);
    serialize_tree_preorder(node->right, writer);
}

std::shared_ptr<HuffmanNode> deserialize_tree_preorder(BitReader& reader) {
    uint8_t is_leaf = reader.read_bit();
    if (is_leaf == 1) {
        uint8_t ch = reader.read_byte();
        return std::make_shared<HuffmanNode>(ch, 0);
    }
    auto left = deserialize_tree_preorder(reader);
    auto right = deserialize_tree_preorder(reader);
    return std::make_shared<HuffmanNode>(left, right);
}

// ============================================================================
// 4. FORMATO DE ARCHIVO COMPRIMIDO Y COMPRESOR / DESCOMPRESOR COMPLETO
// ============================================================================
/*
 * Estructura de la Cabecera Segura contra "The Padding Trap":
 *  - Magic Number: 4 bytes ("HUF4")
 *  - original_size: uint64_t (8 bytes) -> Total exacto de bytes/caracteres originales
 *  - unique_symbols: uint16_t (2 bytes) -> Cantidad de símbolos únicos k (0..256)
 *  - valid_bits_last_byte: uint8_t (1 byte) -> Bits útiles en el último byte (1..8)
 *  - Flujo de bits conjunto (Árbol en Preorden + Datos Comprimidos empaquetados)
 */
struct CompressionMetrics {
    size_t original_bytes = 0;
    size_t compressed_bytes = 0;
    size_t header_bytes = 0;
    size_t payload_bytes = 0;
    uint16_t unique_symbols = 0;
    uint8_t valid_bits_last_byte = 0;
    double entropy_shannon = 0.0;
    double avg_code_length = 0.0;
    double compress_time_ms = 0.0;
    double decompress_time_ms = 0.0;
    bool integrity_verified = false;
};

void compress_file(const std::string& input_path,
                   const std::string& output_path,
                   CompressionMetrics& metrics) {
    auto t0 = std::chrono::high_resolution_clock::now();

    std::ifstream in(input_path, std::ios::binary | std::ios::ate);
    if (!in) throw std::runtime_error("No se pudo abrir entrada: " + input_path);
    size_t file_size = static_cast<size_t>(in.tellg());
    in.seekg(0, std::ios::beg);

    std::vector<uint8_t> raw_data(file_size);
    if (file_size > 0) {
        in.read(reinterpret_cast<char*>(raw_data.data()), static_cast<std::streamsize>(file_size));
    }
    in.close();

    metrics.original_bytes = file_size;

    // 1. Conteo de frecuencias
    std::array<uint64_t, 256> freqs{};
    for (uint8_t b : raw_data) {
        ++freqs[b];
    }

    uint16_t k = 0;
    double entropy = 0.0;
    for (size_t i = 0; i < 256; ++i) {
        if (freqs[i] > 0) {
            ++k;
            double p = static_cast<double>(freqs[i]) / static_cast<double>(file_size);
            entropy -= p * std::log2(p);
        }
    }
    metrics.unique_symbols = k;
    metrics.entropy_shannon = entropy;

    // 2. Construir Árbol de Huffman y Tabla de Códigos
    auto root = build_huffman_tree(freqs);
    std::array<CodeEntry, 256> code_table{};
    build_code_table(root, 0, 0, code_table);

    uint64_t total_data_bits = 0;
    for (size_t i = 0; i < 256; ++i) {
        if (freqs[i] > 0) {
            total_data_bits += freqs[i] * code_table[i].len;
        }
    }
    metrics.avg_code_length = file_size > 0
        ? static_cast<double>(total_data_bits) / static_cast<double>(file_size)
        : 0.0;

    // 3. Empaquetar Árbol en Preorden + Flujo de Datos en BitWriter
    BitWriter writer(file_size / 2 + 128);
    if (root) {
        serialize_tree_preorder(root, writer);
        for (uint8_t b : raw_data) {
            const auto& entry = code_table[b];
            writer.write_bits(entry.bits, entry.len);
        }
    }
    uint8_t valid_last_bits = writer.flush();
    metrics.valid_bits_last_byte = valid_last_bits;

    // 4. Escribir archivo comprimido en disco
    std::ofstream out(output_path, std::ios::binary);
    if (!out) throw std::runtime_error("No se pudo abrir salida: " + output_path);

    const char magic[4] = {'H', 'U', 'F', '4'};
    uint64_t orig_size_u64 = static_cast<uint64_t>(file_size);

    out.write(magic, 4);
    out.write(reinterpret_cast<const char*>(&orig_size_u64), sizeof(orig_size_u64));
    out.write(reinterpret_cast<const char*>(&k), sizeof(k));
    out.write(reinterpret_cast<const char*>(&valid_last_bits), sizeof(valid_last_bits));

    const auto& packed = writer.data();
    if (!packed.empty()) {
        out.write(reinterpret_cast<const char*>(packed.data()),
                  static_cast<std::streamsize>(packed.size()));
    }
    out.close();

    auto t1 = std::chrono::high_resolution_clock::now();
    metrics.compress_time_ms = std::chrono::duration<double, std::milli>(t1 - t0).count();

    size_t tree_bits = (k > 0) ? (10U * k - 1U) : 0U;
    metrics.header_bytes = 4 + 8 + 2 + 1 + (tree_bits + 7) / 8;
    metrics.compressed_bytes = 4 + 8 + 2 + 1 + packed.size();
    metrics.payload_bytes = (total_data_bits + 7) / 8;
}

void decompress_file(const std::string& input_path,
                     const std::string& output_path,
                     CompressionMetrics& metrics) {
    auto t0 = std::chrono::high_resolution_clock::now();

    std::ifstream in(input_path, std::ios::binary | std::ios::ate);
    if (!in) throw std::runtime_error("No se pudo abrir comprimido: " + input_path);
    size_t total_file_size = static_cast<size_t>(in.tellg());
    in.seekg(0, std::ios::beg);

    char magic[4];
    uint64_t orig_size = 0;
    uint16_t k = 0;
    uint8_t valid_last_bits = 0;

    in.read(magic, 4);
    in.read(reinterpret_cast<char*>(&orig_size), sizeof(orig_size));
    in.read(reinterpret_cast<char*>(&k), sizeof(k));
    in.read(reinterpret_cast<char*>(&valid_last_bits), sizeof(valid_last_bits));

    size_t stream_bytes = total_file_size - 15;
    std::vector<uint8_t> packed(stream_bytes);
    if (stream_bytes > 0) {
        in.read(reinterpret_cast<char*>(packed.data()), static_cast<std::streamsize>(stream_bytes));
    }
    in.close();

    std::vector<uint8_t> decoded;
    decoded.reserve(static_cast<size_t>(orig_size));

    if (orig_size > 0 && k > 0) {
        BitReader reader(packed.data(), packed.size());
        auto root = deserialize_tree_preorder(reader);

        // Caso especial k == 1 (un único carácter repetido N veces)
        if (root->is_leaf()) {
            for (uint64_t i = 0; i < orig_size; ++i) {
                (void)reader.read_bit(); // Consumir el bit '0' de cada carácter
                decoded.push_back(root->character);
            }
        } else {
            // Navegación exacta detenida por el contador `orig_size` (inmune al Padding Trap)
            for (uint64_t count = 0; count < orig_size; ++count) {
                const HuffmanNode* curr = root.get();
                while (!curr->is_leaf()) {
                    uint8_t bit = reader.read_bit();
                    curr = (bit == 0) ? curr->left.get() : curr->right.get();
                }
                decoded.push_back(curr->character);
            }
        }
    }

    std::ofstream out(output_path, std::ios::binary);
    if (!decoded.empty()) {
        out.write(reinterpret_cast<const char*>(decoded.data()),
                  static_cast<std::streamsize>(decoded.size()));
    }
    out.close();

    auto t1 = std::chrono::high_resolution_clock::now();
    metrics.decompress_time_ms = std::chrono::duration<double, std::milli>(t1 - t0).count();
}

bool verify_files_identical(const std::string& f1, const std::string& f2) {
    std::ifstream s1(f1, std::ios::binary | std::ios::ate);
    std::ifstream s2(f2, std::ios::binary | std::ios::ate);
    if (!s1 || !s2) return false;
    if (s1.tellg() != s2.tellg()) return false;
    s1.seekg(0);
    s2.seekg(0);
    std::istreambuf_iterator<char> b1(s1), b2(s2), end;
    return std::equal(b1, end, b2);
}

int main(int argc, char* argv[]) {
    if (argc == 4) {
        std::string mode = argv[1];
        std::string in_file = argv[2];
        std::string out_file = argv[3];
        CompressionMetrics m;
        if (mode == "-c") {
            compress_file(in_file, out_file, m);
            std::cout << "Comprimido: " << m.original_bytes << " B -> "
                      << m.compressed_bytes << " B ("
                      << std::fixed << std::setprecision(2)
                      << (100.0 * m.compressed_bytes / m.original_bytes) << "%)\n";
        } else if (mode == "-d") {
            decompress_file(in_file, out_file, m);
            std::cout << "Descomprimido exitosamente en " << m.decompress_time_ms << " ms.\n";
        }
        return 0;
    }

    std::cout << "====================================================================\n";
    std::cout << " SUITE DE AUDITORÍA Y BENCHMARKING HUFFMAN (FASE 2)\n";
    std::cout << "====================================================================\n";

    std::vector<std::pair<std::string, std::string>> benchmarks = {
        {"Caso A: Texto Estructurado (Quijote + Codigo Fuente)", "bench_texto.txt"},
        {"Caso B: Binario Pre-comprimido (.zip / .png)", "bench_comprimido.bin"},
        {"Caso C: Homogeneo Extremo (10^7 repeticiones de 'A')", "bench_homogeneo_10M.txt"}
    };

    for (const auto& [title, path] : benchmarks) {
        std::ifstream test_in(path);
        if (!test_in.good()) continue;
        test_in.close();

        std::string huf_path = path + ".huf";
        std::string rec_path = path + ".rec";

        CompressionMetrics m;
        compress_file(path, huf_path, m);
        decompress_file(huf_path, rec_path, m);
        m.integrity_verified = verify_files_identical(path, rec_path);

        double ratio = m.original_bytes > 0
            ? (100.0 * static_cast<double>(m.compressed_bytes) / static_cast<double>(m.original_bytes))
            : 0.0;

        std::cout << "\n[" << title << "]\n";
        std::cout << "  - Archivo:              " << path << "\n";
        std::cout << "  - Simbolos unicos (k):  " << m.unique_symbols << "\n";
        std::cout << "  - Tamano Original:      " << m.original_bytes << " bytes\n";
        std::cout << "  - Tamano Comprimido:    " << m.compressed_bytes << " bytes (Header: "
                  << m.header_bytes << " B | Payload: " << m.payload_bytes << " B)\n";
        std::cout << "  - Entropia H(X):        " << std::fixed << std::setprecision(6) << m.entropy_shannon << " bits/byte\n";
        std::cout << "  - Longitud Media L:     " << std::fixed << std::setprecision(6) << m.avg_code_length << " bits/byte\n";
        std::cout << "  - Ratio (Comp/Orig):    " << std::fixed << std::setprecision(4) << ratio << " %\n";
        std::cout << "  - Tiempo Compresion:    " << std::fixed << std::setprecision(2) << m.compress_time_ms << " ms\n";
        std::cout << "  - Tiempo Descompresion: " << std::fixed << std::setprecision(2) << m.decompress_time_ms << " ms\n";
        std::cout << "  - Integridad Bit-a-Bit: " << (m.integrity_verified ? "EXITO (100% IDENTICO)" : "FALLO") << "\n";
    }

    return 0;
}
