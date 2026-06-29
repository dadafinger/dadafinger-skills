// 매뉴얼 이미지 일괄 OCR (macOS Vision)
// 사용법: swift ocr_vision.swift <mediaDir> <outPath.jsonl> [언어들(쉼표, 기본 "ko-KR,en-US")]
// 일본어 매뉴얼은 "ja-JP,en-US" 지정. usesLanguageCorrection은 IP/호스트명 보존을 위해 끔.
import Foundation
import Vision
import AppKit

let args = CommandLine.arguments
guard args.count >= 3 else {
    FileHandle.standardError.write("usage: swift ocr_vision.swift <mediaDir> <out.jsonl> [langs]\n".data(using: .utf8)!)
    exit(1)
}
let mediaDir = args[1]
let outPath = args[2]
let langs = args.count >= 4 ? args[3].split(separator: ",").map(String.init) : ["ko-KR", "en-US"]

let fm = FileManager.default
let files = try fm.contentsOfDirectory(atPath: mediaDir).sorted()
var out = ""
var done = 0

for f in files {
    let path = mediaDir + "/" + f
    guard let img = NSImage(contentsOfFile: path),
          let cg = img.cgImage(forProposedRect: nil, context: nil, hints: nil) else {
        FileHandle.standardError.write("skip \(f)\n".data(using: .utf8)!)
        continue
    }
    let request = VNRecognizeTextRequest()
    request.recognitionLevel = .accurate
    request.recognitionLanguages = langs
    request.usesLanguageCorrection = false
    let handler = VNImageRequestHandler(cgImage: cg, options: [:])
    try? handler.perform([request])
    let texts = (request.results ?? []).compactMap { $0.topCandidates(1).first?.string }
    let obj: [String: String] = ["file": f, "text": texts.joined(separator: "\n")]
    if let data = try? JSONSerialization.data(withJSONObject: obj),
       let s = String(data: data, encoding: .utf8) {
        out += s + "\n"
    }
    done += 1
    if done % 25 == 0 {
        FileHandle.standardError.write("progress \(done)/\(files.count)\n".data(using: .utf8)!)
        try? out.write(toFile: outPath, atomically: true, encoding: .utf8)
    }
}
try out.write(toFile: outPath, atomically: true, encoding: .utf8)
print("done \(done)/\(files.count) -> \(outPath)")
