import os
import dropbox

# Replace with your generated access token
ACCESS_TOKEN = "sl.u.AFkyjdi9Zw7GIPBCk2rSBQUrQPNGC9FQPiNN5UEtqPJq9eA0-qsjAlftw5a3BoTcepV8xWbqBvE7nclDVgdiGtPtimDvpGRkXezo6TlAD_ZlByxlfYpi6x5dnMIyXZES3oudgk_HTnIVDi8oHTdwxD59s1p_JVkml3uhUlPD0fIl3VVn4qK8Bs0LQTgTHdSK7CSk-dKr0aGTP9KJnofAGjH_kvJhsTSm7nR0xOyEIJIZ0Ql0V6xv4dFnp5PypeCqS7Yqf_3Czpz3fvnQurX7NBfu_ZhyhkbpbRmwSEsPsVJPIPDAy0JnHN1R3Nzwdk2IodJt9zewUTP30rVDHbxDrcnVLF1y6ocFGx_-nOx6ZXfW0WzrsCdmhxZEPXmg5kij5P6kdVsagLujs-m6c86Z6jW1kcuenEfS-VN69P60ZS8_rK_9GK20B7l1E8X2aAJPbG6SNJmWCCdt8IWJOm7Tkb8nycGuwDkqU2wF8LTKsFSelYagxn_5gaSv98d0QaCq7UQoCb46L3MgG-obl__uxQ5KSxs5rlZx-hJyZqpkxRl_bjqoQbxeFZfbBL4tbF4OJb5YfT3WTGIw0R87Iazt48nYVBRZZl4t-dwIh1X64wrvE4D-Gz9mYBfq-LbRV4sc5QWW3oy2bnQdmQS3wEddhzCyt_msvj4ir9RPzmEDL6nbxVG2QGpxLylnqTTbLsEwZT0XLYAs6MBj3nrT464J5KvVQzSuDpW4wrUeJILSG1gaEioaGwXTi5L1mWMPn4BIFKRfQPsTtiQqxje9tFlL-BPpmDUHYoDrfyJZtqo4lIcDJFWXYqFEqeEMATXoQm9VxeZHHemHOtYY8OGHs9NlUOvNmrO2vm7Lmhep_sJJkZuUORvDVt1QcjatdQUc9R-yJnkrA_k1LWNJL713oGo8OFZWhJghnBsKPI5crrOcbBGdWyRXOfgUr9NlBK17ypSVLjz-E6wGcT9dj0ch9NtC6WORIGZFM85-5Our7KXDUV1eKWZaJuHgHzx_8hUlw4wZvLmzo0cPQgNwLhJ_rxdJ2Zu9Na3SJxB6wT4ScpVTpCOBOX0xn64mjT1LUk_xJ5viMZkQCAGueEgxShkEaIezaW9_qCBSPsZ_KWE10KLZJfXvX2s2vhi6u9hRoAqZfrcJt5pzYOOZKQLq_LDWY-xgUZKbLD-px8lFkr26xR4wXrIwrTNMtJeycrDtoOQZQSHAED6mWhfIFwpvBwIj0qByWF41DYQboRHsVGdPeqLROTzkNrdn1n7OB34pI0AqNtPR_AXYJunt-Vvknf6KAnj96OpZ9ZJW1gjEfKEPHrPHn-uotxbg7NDSjFNpd44s_HYSq-c:AUS"

def upload_file(local_path, dropbox_path):
    dbx = dropbox.Dropbox(ACCESS_TOKEN)
    
    with open(local_path, "rb") as f:
        file_size = os.path.getsize(local_path)
        chunk_size = 150 * 1024 * 1024  # 150MB chunks (good for large files)
        
        if file_size <= chunk_size:
            dbx.files_upload(f.read(), dropbox_path)
        else:
            upload_session_start = dbx.files_upload_session_start(f.read(chunk_size))
            cursor = dropbox.files.UploadSessionCursor(session_id=upload_session_start.session_id, offset=f.tell())
            commit = dropbox.files.CommitInfo(path=dropbox_path)

            while f.tell() < file_size:
                if (file_size - f.tell()) <= chunk_size:
                    dbx.files_upload_session_finish(f.read(chunk_size), cursor, commit)
                else:
                    dbx.files_upload_session_append(f.read(chunk_size), cursor.session_id, cursor.offset)
                    cursor.offset = f.tell()

upload_file(r"X:\The Thing Interview - Mar 2025\URSA\A006_02270042_C001.braw", "/CLI Uploads/file.ext")
