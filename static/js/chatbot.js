const chatBox = document.getElementById("chat-box");
const input = document.getElementById("user-input");
const button = document.getElementById("send-btn");

button.addEventListener("click", kirimPesan);

input.addEventListener("keypress", function(e){

    if(e.key==="Enter"){

        kirimPesan();

    }

});

function kirimPesan(){

    const teks = input.value.trim();

    if(teks==="") return;

    chatBox.innerHTML += `
        <div class="user-message">
            ${teks}
        </div>
    `;

    chatBox.scrollTop = chatBox.scrollHeight;

    fetch("/prediksi",{

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify({
            teks:teks
        })

    })

    .then(res=>res.json())

    .then(data=>{

        chatBox.innerHTML += `

        <div class="bot-message">

            <b>Kategori:</b>
            <p>${data.kategori}</p>

            <hr>

            <b>💡 Solusi Awal</b>
            <p style="white-space:pre-line">
                ${data.solusi}
            </p>

            <small>
            *Solusi di atas merupakan rekomendasi awal dari CampusVoice AI.
            Jika masalah belum terselesaikan, Anda dapat mengirim laporan kepada pihak kampus.
            </small>

            <br><br>

            <button class="selesai-btn">
                😊 Masalah Sudah Selesai
            </button>

            <button class="kirim-btn">

                Kirim Keluhan

            </button>

        </div>

        `;

        chatBox.scrollTop = chatBox.scrollHeight;

        const kirimButton = document.querySelectorAll(".kirim-btn");
        const selesaiButton = document.querySelectorAll(".selesai-btn");

        const btnKirim = kirimButton[kirimButton.length-1];
        const btnSelesai = selesaiButton[selesaiButton.length-1];

        btnSelesai.addEventListener("click",function(){

            chatBox.innerHTML += `

            <div class="bot-message">

            😊 Senang mendengar masalah Anda telah terselesaikan.
            Terima kasih telah menggunakan CampusVoice.

            </div>

            `;

            chatBox.scrollTop = chatBox.scrollHeight;

            btnSelesai.disabled=true;
            btnKirim.disabled=true;

        });

        btnKirim.addEventListener("click",function(){

            fetch("/simpan_keluhan",{

                method:"POST",

                headers:{
                    "Content-Type":"application/json"
                },

                body:JSON.stringify({

                    teks:teks,

                    kategori:data.kategori

                })

            })

            .then(res=>res.json())

            .then(res=>{

                chatBox.innerHTML += `

                <div class="bot-message">
                Keluhan berhasil dikirim.
                Anda dapat memantau prosesnya melalui menu Riwayat Keluhan.
                </div>

                `;

                chatBox.scrollTop = chatBox.scrollHeight;

                btnSelesai.disabled=true;
                btnKirim.disabled=true;

            });

        });

    });

    input.value="";

}