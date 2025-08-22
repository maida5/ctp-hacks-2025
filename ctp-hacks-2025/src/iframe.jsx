// courtesy to spotify example: https://developer.spotify.com/documentation/embeds/playgrounds/iFrameAPI

import { useRef, useState, useEffect } from "react";

const Iframe = (props) => {
    const embedRef = useRef(null);
    const spotifyEmbedControllerRef = useRef(null);
    const [iFrameAPI, setIFrameAPI] = useState(undefined);
    const [playerLoaded, setPlayerLoaded] = useState(false);
    const [uri, setUri] = useState(props.uri);

    useEffect(() => {
        const script = document.createElement("script");
        script.src = "https://open.spotify.com/embed/iframe-api/v1";
        script.async = true;
        document.body.appendChild(script);
        return () => {
            document.body.removeChild(script);
        };
    }, []);

    useEffect(() => {
        if (iFrameAPI) {
            return;
        }

        window.onSpotifyIframeApiReady = (SpotifyIframeApi) => {
            setIFrameAPI(SpotifyIframeApi);
        };
    }, [iFrameAPI]);

    useEffect(() => {
        if (playerLoaded || iFrameAPI === undefined) {
            return;
        }

        iFrameAPI.createController(
            embedRef.current,
            {
                width: "100%",
                height: "352",
                uri: uri,
            },
            (spotifyEmbedController) => {
                spotifyEmbedController.addListener("ready", () => {
                    setPlayerLoaded(true);
                });

                const handlePlaybackUpdate = (e) => {
                    const { position, duration, isBuffering, isPaused, playingURI } =
                        e.data;
                    console.log(
                        `Playback State updates:
            position - ${position},
            duration - ${duration},
            isBuffering - ${isBuffering},
            isPaused - ${isPaused},
            playingURI - ${playingURI},
            duration - ${duration}`
                    );
                };

                spotifyEmbedController.addListener(
                    "playback_update",
                    handlePlaybackUpdate
                );

                spotifyEmbedController.addListener("playback_started", (e) => {
                    const { playingURI } = e.data;
                    console.log(`The playback has started for: ${playingURI}`);
                });

                spotifyEmbedControllerRef.current = spotifyEmbedController;
            }
        );

        return () => {
            if (spotifyEmbedControllerRef.current) {
                spotifyEmbedControllerRef.current.removeListener("playback_update");
            }
        };
    }, [playerLoaded, iFrameAPI, uri]);

    const onPauseClick = () => {
        if (spotifyEmbedControllerRef.current) {
            spotifyEmbedControllerRef.current.pause();
        }
    };

    const onPlayClick = () => {
        if (spotifyEmbedControllerRef.current) {
            spotifyEmbedControllerRef.current.play();
        }
    };

    return (
        <div>
            <div ref={embedRef} />
            {!playerLoaded && <p>Loading...</p>}
        </div >
    );
}

export default Iframe;
