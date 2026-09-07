# Facebook Post: The Illusion of Obsidian & Why Knowledge Graphs Need File Governance

> **Author**: Than Bui  
> **Topic**: File Governance, Obsidian Anti-patterns, and Knowledge Graph Integration  
> **Status**: Ready for Social Publishing  
> **Disclaimers**: For reference and community discussion only.  
> **Open-Source Repository**: https://github.com/productaivn-wq/FileGovernance-Skill

---

## 🇺🇸 Version 1: English (Global Tech / Builder Community)

```markdown
Most people using Obsidian (and coding in general) are trapped in an illusion.

You’ve seen the screenshots: someone proudly sharing an Obsidian graph view with 2,000 glowing dots and thousands of crisscrossing lines. It looks like a cyberpunk neural network.

The reality? Most of those vaults are unnavigable digital junkyards. 
People hoard notes, link [[random_ideas]] together, and create clutter with zero governance.

The same thing happens in developers’ codebases:
Dozens of loose files (`test_v2.py`, `notes.md`, `temp_draft.ts`) buried in arbitrary nested folders where neither humans—nor autonomous AI agents—can tell what is active production truth, what is a draft, and what is dead.

Here is the fundamental law:
👉 A Knowledge Graph cannot fix file chaos. Files require GOVERNANCE before they can become NODES.

To solve this, you need to understand two very different layers:

1. Organizing by Lifecycle is just a file management style.
Lifecycle organization is simply managing operational state:
Is this an incoming raw note? An active sprint deliverable? A reusable reference? Or an archived record?
It keeps your workspace flat, clean, and avoids folder mazes.

2. A Knowledge Graph is about relationships and meaning.
A Knowledge Graph doesn't care which folder a file sits in. It cares about concepts:
How does this architecture spec relate to that database schema? Which decision superseded that previous design?

Why do they need each other?
Because if you feed an AI or GraphRAG system an unorganized pile of files without lifecycle awareness, you get the "Outdated Truth" trap:
The AI reads an abandoned 2-year-old brainstorm with the exact same weight as today's active production spec!

When you bring basic governance to your files—giving them consistent, structured names and clear operational statuses:
• Your files naturally become clean, unambiguous Nodes in a Knowledge Graph.
• Lineage relationships (Research ➔ Design ➔ Code ➔ Test) are immediately understood by AI without guessing.
• AI agents can execute exact graph queries instead of relying on fuzzy vector similarity.

---

📌 NOTE: This post is for reference and community discussion only. 

I ended up having to formulate this framework because when building autonomous agent workflows, I searched everywhere for a ready-made repository to "steal with pride"—and couldn't find one that bridged file system hygiene directly to Knowledge Graphs. 

However, this isn't invented out of thin air. It draws inspiration from decades of proven principles:
• Library Classification & Faceted Taxonomies (Ranganathan’s PMEST, Dewey Decimal, UDC)
• Archival Science & Records Management (ISO 15489 - active vs. continuous vs. archival retention)
• Engineering Information Management (ISO 19650 structured naming)
• Johnny.Decimal & Tiago Forte's P.A.R.A
• W. Edwards Deming’s PDCA (Plan-Do-Check-Act) artifact cycles

I've packaged the complete Skill definition, reference documents, and copy-paste LLM prompt into an open-source repo:
👉 GitHub: (Link in the first comment 👇)

If you know of any open-source repositories, academic papers, or battle-tested industry standards tackling this—or if you have thoughts, feedback, or critiques—please tell me in the comments! Let’s compare notes. 👇
```

---

## 🇻🇳 Version 2: Vietnamese (Tech Community / Founders & Builders)

```markdown
Hầu hết anh em xài Obsidian (và cả anh em code) đều đang bị dính một "cú lừa" mang tên: Graph View.

Anh em chắc chắn từng thấy những bài flex ảnh chụp Obsidian: một "dải ngân hà" lung linh với 2.000 - 3.000 chấm tròn nối chằng chịt vào nhau. Trông cực kỳ tri thức và nguy hiểm.

Nhưng thực tế thì sao? 
Đa số những chiếc vault đó là một bãi rác số được liên kết dây điện chằng chịt. Người ta gom góp note vô tội vạ, link loạn xạ, để rồi sau 3 tháng không ai—kể cả AI—tìm lại được đâu là thông tin chính xác.

Bên folder làm việc hay repo code của anh em cũng vậy:
File đặt tên theo cảm tính, tài liệu nháp nằm lẫn với tài liệu sản phẩm, không ai biết cái nào là bản chốt, cái nào đã bỏ đi.

Vấn đề cốt lõi ở đây là:
👉 Knowledge Graph không thể giải quyết được sự bừa bộn của file system. File mà không có QUẢN TRỊ (Governance), thì Graph của anh em chỉ là một mạng lưới hỗn loạn.

Muốn xây dựng hệ thống tài liệu và code chuẩn chỉnh, anh em phải phân biệt rõ 2 tầng:

1. Quản lý theo Lifecycle (Vòng đời) chỉ là phong cách sắp xếp file:
Nó chỉ đơn thuần quản lý trạng thái vận hành: File này đang là tài liệu nháp, đang trong dự án chạy nước rút, là tài liệu tham khảo lâu dài, hay đã đóng băng lưu trữ? 
Lifecycle giúp dọn dẹp workspace gọn gàng, dẹp bỏ các mê cung thư mục lồng nhau.

2. Knowledge Graph là tầng liên kết ngữ nghĩa:
Graph không quan tâm file nằm ở ổ đĩa nào, nó quan tâm đến bản chất: Bản thiết kế này liên quan đến service nào? Quyết định kỹ thuật này thay thế cho giải pháp cũ nào?

Tại sao cần kết hợp cả hai?
Nếu anh em cắm AI hoặc GraphRAG vào một mớ file lộn xộn không có quản trị vòng đời, AI sẽ dính ngay lỗi "Ảo giác dữ liệu cũ":
Nó sẽ lôi một ý tưởng bị vứt xó từ 2 năm trước ra trả lời với độ uy tín ngang ngửa bản spec vừa duyệt sáng nay.

Khi file của anh em có quy chuẩn đặt tên nhất quán và trạng thái rõ ràng:
• Mỗi file tự khắc trở thành một Node chuẩn xác trong Knowledge Graph.
• Mạch phát triển (từ nghiên cứu ➔ thiết kế ➔ code ➔ kiểm thử) hiện ra tự nhiên mà AI không cần phải "đoán mò".
• AI Agent có thể truy vấn chính xác từng dữ liệu thay vì vector search hên xui.

---

📌 LƯU Ý: Bài viết này chia sẻ hoàn toàn với mục đích tham khảo và trao đổi học hỏi.

Mình đúc kết mô hình này xuất phát từ nhu cầu thực tế khi xây dựng hệ thống cho AI Agent: lùng sục khắp nơi nhưng không tìm thấy một repo mở nào có sẵn để "steal with pride" (kế thừa tự hào) nhằm giải quyết trọn vẹn cầu nối giữa tổ chức file và Knowledge Graph.

Tuy nhiên, mô hình này không tự nhiên sinh ra từ hư không, mà kế thừa từ rất nhiều nền tảng kinh điển:
• Khoa học thư viện & phân loại đa diện (Ranganathan PMEST, Dewey Decimal, UDC)
• Khoa học lưu trữ & Quản trị hồ sơ (Tiêu chuẩn ISO 15489 về vòng đời tài liệu)
• Tiêu chuẩn quản lý thông tin kỹ thuật (ISO 19650)
• Phương pháp Johnny.Decimal và P.A.R.A của Tiago Forte
• Chu trình chất lượng PDCA (Plan-Do-Check-Act) của W. Edwards Deming

Toàn bộ Skill này (kèm tài liệu chi tiết và Prompt mẫu cho ChatGPT / Claude) mình đã đóng gói thành repo mở tại đây:
👉 GitHub: (Link mình để ngay ở comment đầu tiên bên dưới nhé 👇)

Anh em có biết repo mã nguồn mở nào, bài báo khoa học hay chuẩn công nghiệp nào giải quyết vấn đề này xịn hơn không? Hoặc anh em có góc nhìn, phản biện hay góp ý nào, chia sẻ cho mình bên dưới nhé! Rất mong được cùng thảo luận với mọi người. 👇
```
