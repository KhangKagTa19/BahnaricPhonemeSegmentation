    file_name = "/workspaces/bahnaric-phoneme/src/grưa.wav"
    signal, sr = librosa.load(file_name.replace("TextGrid", "wav"), sr=16000)

    feature_dfs = []
    for k in range(5):
        # Define window size
        k = 75 + (1 + k) * 10
        assert k % 2 == 1, "k must be odd"

        # Break audio into frames
        frame_length = int(sr * 0.005)  # 5ms
        hop_length = int(sr * 0.001)  # 1ms
        frames = librosa.util.frame(
            signal, frame_length=frame_length, hop_length=hop_length
        )

        # Pad frames at the beginning and end
        padding = (k - 1) // 2
        padded_frames = np.pad(frames, ((0, 0), (padding, padding)), mode="edge")

        # Calculate features on sliding window of k frames
        features = []
        for i in range(padding, len(padded_frames[0]) - padding):
            window = padded_frames[:, i - padding : i + padding + 1]
            feature = extract_feature_means(signal=window.flatten(), sr=sr)
            features.append(feature)

        features = pd.concat(features, axis=0)
        features.columns = [f"{col}_w{str(k).zfill(3)}" for col in features.columns]
        feature_dfs.append(features)

    test_features = pd.concat(feature_dfs, axis=1)
