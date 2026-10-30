# TuffNSh3ll
TuffNShell is a modular Python-based toolkit that bridges WebSocket connections with local TCP ports using Cloudflare Tunnels. It features multi-layer obfuscation, silent background execution, automated OS detection, and an integrated interactive listener with clean formatting.

 This tool was created purely for educational purposes,
 self-authorized penetration testing, and network security simulation
 within an environment with legitimate permission.
 Any misuse of this tool outside of legitimate authorization is
 entirely the responsibility of the user.


Tools ini dibuat murni untuk tujuan edukasi,
 pengujian penetrasi mandiri (penetration testing),
 dan simulasi keamanan jaringan dalam lingkungan yang memiliki izin
 sah. Penyalahgunaan tools ini di luar izin yang sah sepenuhnya
 merupakan tanggung jawab pengguna.


                     ###   PANDUAN   ###

STEP BY STEP (3 tab)

DI SISI PENYERANG

tab terminal 1: Jalankan server.py
tab terminal 2: Jalankan command berikut -->
          cloudflared tunnel --url http://localhost:8081

tab terminal 3: Jalankan generate.py

 Biarkan korban menjalankan 'client.py' tadi
      biarkan koneksi TCP
               Dan reverse shell terhubung.

------------------------------------------------------------
                       # ENGLISH #
Step By Step (3 tab)

tab 1: run server.py
tab 2:run cloudflared tunnel --url http://localhost:8081
tab 3:run generate.py

let the victim run "client.py" and finish

-----------------------------------------------------------
