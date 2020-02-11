#!/bin/bash
i=0
for fi in sho_?.JPG; do
    mv "$fi" sho_0$i.JPG
    i=$((i+1))
done

