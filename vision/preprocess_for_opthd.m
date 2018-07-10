function P = preprocess_for_opthd(I)
[row, col, ~] = size(I);
P = zeros(row, col);

% histogram & sum
histogram = zeros(1, 256);
for i = 1:row
    for t = 1:col
        histogram(1, I(i, t) + 1) = histogram(1, I(i, t) + 1) + 1;
    end
end

% ave
sum = 0;
for i = 1:256
    sum = sum + i * histogram(i);
end

% iterations
ave = sum / (row * col);
T = ave;
border = int32(T);
if border > ave
    border = border - 1;
end
iter_tag = 1;
u0 = 0;
u1 = 0;

while iter_tag
    sum0 = 0;
    sum1 = 0;
    count0 = 0;
    count1 = 0;
    for t = 1:border
        sum0 = sum0 + t * histogram(1, t);
        count0 = count0 + histogram(1, t);
    end
    for t = (border + 1):256
        sum1 = sum1 + t * histogram(1, t);
        count1 = count1 + histogram(1, t);
    end
    ave0 = sum0 / count0;
    ave1 = sum1 / count1;
    if abs(ave0 - u0) < 0.001 || abs(ave1 - u1) < 0.001
        iter_tag = 0;
    else
        T = (ave0 + ave1) / 2;
        border = int32(T);
        if border > T
            border = border - 1;
        end
        u0 = ave0;
        u1 = ave1;
    end
end

% process
for i = 1:row
    for j = 1:col
        if I(i, j) < T
            P(i, j) = 0;
        else
            P(i, j) =255;
        end
    end
end

imshow(P)