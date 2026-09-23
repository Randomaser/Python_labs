procedure InitializeComponent;
    begin
        self.comboBox1 := new System.Windows.Forms.ComboBox();
        self.comboBox2 := new System.Windows.Forms.ComboBox();
        self.button1 := new System.Windows.Forms.Button();
        self.label1 := new System.Windows.Forms.Label();
        self.label2 := new System.Windows.Forms.Label();
        self.comboBox3 := new System.Windows.Forms.ComboBox();
        self.label3 := new System.Windows.Forms.Label();
        self.label4 := new System.Windows.Forms.Label();
        self.label5 := new System.Windows.Forms.Label();
        self.label6 := new System.Windows.Forms.Label();
        self.label7 := new System.Windows.Forms.Label();
        self.label8 := new System.Windows.Forms.Label();
        self.button2 := new System.Windows.Forms.Button();
        self.label9 := new System.Windows.Forms.Label();
        self.button3 := new System.Windows.Forms.Button();
        self.label10 := new System.Windows.Forms.Label();
        self.button4 := new System.Windows.Forms.Button();
        self.button5 := new System.Windows.Forms.Button();
        self.button6 := new System.Windows.Forms.Button();
        self.label11 := new System.Windows.Forms.Label();
        self.SuspendLayout();
        // 
        // comboBox1
        // 
        self.comboBox1.Items.AddRange(new System.Object[17]('', 'TimSort', 'Болотная (только 10 эл.)', 'Быстрая', 'Вставками', 'Гномья', 'Деревом', 'Методом выбора', 'Перемешиванием', 'Пирамидальная', 'Плавная', 'Подсчётом', 'Поразрядная', 'Пузырьком', 'Расчёской', 'Слиянием', 'Шелла'));
        self.comboBox1.Location := new System.Drawing.Point(155, 125);
        self.comboBox1.Name := 'comboBox1';
        self.comboBox1.Size := new System.Drawing.Size(139, 24);
        self.comboBox1.Sorted := true;
        self.comboBox1.TabIndex := 0;
        self.comboBox1.Visible := false;
        self.comboBox1.SelectedIndexChanged += comboBox1_SelectedIndexChanged;
        // 
        // comboBox2
        // 
        self.comboBox2.Items.AddRange(new System.Object[4]('', 'Мало (64)', 'Средне (1000)', 'Много (10000-100000)'));
        self.comboBox2.Location := new System.Drawing.Point(155, 155);
        self.comboBox2.Name := 'comboBox2';
        self.comboBox2.Size := new System.Drawing.Size(139, 24);
        self.comboBox2.TabIndex := 1;
        self.comboBox2.Visible := false;
        self.comboBox2.SelectedIndexChanged += comboBox2_SelectedIndexChanged;
        // 
        // button1
        // 
        self.button1.Location := new System.Drawing.Point(155, 215);
        self.button1.Name := 'button1';
        self.button1.Size := new System.Drawing.Size(139, 35);
        self.button1.TabIndex := 2;
        self.button1.Text := 'Отсортировать';
        self.button1.UseVisualStyleBackColor := true;
        self.button1.Visible := false;
        self.button1.Click += button1_Click;
        // 
        // label1
        // 
        self.label1.AutoSize := true;
        self.label1.Font := new System.Drawing.Font('Microsoft Sans Serif', 10.2, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, (System.Byte(204)));
        self.label1.Location := new System.Drawing.Point(330, 125);
        self.label1.Name := 'label1';
        self.label1.Size := new System.Drawing.Size(118, 20);
        self.label1.TabIndex := 3;
        self.label1.Text := 'Результат: ';
        self.label1.Visible := false;
        // 
        // label2
        // 
        self.label2.Font := new System.Drawing.Font('Microsoft Sans Serif', 10.2, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, (System.Byte(204)));
        self.label2.ForeColor := System.Drawing.Color.Red;
        self.label2.Location := new System.Drawing.Point(373, 126);
        self.label2.Name := 'label2';
        self.label2.Size := new System.Drawing.Size(203, 83);
        self.label2.TabIndex := 4;
        self.label2.Text := 'Вы выбрали неверные значения!';
        self.label2.TextAlign := System.Drawing.ContentAlignment.MiddleCenter;
        self.label2.Visible := false;
        self.label2.Click += label2_Click;
        // 
        // comboBox3
        // 
        self.comboBox3.FormattingEnabled := true;
        self.comboBox3.Items.AddRange(new System.Object[4]('', 'Лучший', 'Средний', 'Худший'));
        self.comboBox3.Location := new System.Drawing.Point(155, 185);
        self.comboBox3.Name := 'comboBox3';
        self.comboBox3.Size := new System.Drawing.Size(139, 24);
        self.comboBox3.TabIndex := 5;
        self.comboBox3.Visible := false;
        // 
        // label3
        // 
        self.label3.AutoSize := true;
        self.label3.Font := new System.Drawing.Font('Microsoft Sans Serif', 10.2, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, (System.Byte(204)));
        self.label3.Location := new System.Drawing.Point(330, 185);
        self.label3.Name := 'label3';
        self.label3.Size := new System.Drawing.Size(277, 20);
        self.label3.TabIndex := 6;
        self.label3.Text := 'Всего количество операций:';
        self.label3.Visible := false;
        // 
        // label4
        // 
        self.label4.AutoSize := true;
        self.label4.Font := new System.Drawing.Font('Microsoft Sans Serif', 10.2, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, (System.Byte(204)));
        self.label4.Location := new System.Drawing.Point(330, 155);
        self.label4.Name := 'label4';
        self.label4.Size := new System.Drawing.Size(14, 20);
        self.label4.TabIndex := 7;
        self.label4.Text := ' ';
        self.label4.Visible := false;
        self.label4.Click += label4_Click;
        // 
        // label5
        // 
        self.label5.AutoSize := true;
        self.label5.Font := new System.Drawing.Font('Microsoft Sans Serif', 10.2, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, (System.Byte(204)));
        self.label5.Location := new System.Drawing.Point(330, 215);
        self.label5.Name := 'label5';
        self.label5.Size := new System.Drawing.Size(0, 20);
        self.label5.TabIndex := 8;
        self.label5.Visible := false;
        // 
        // label6
        // 
        self.label6.Location := new System.Drawing.Point(63, 121);
        self.label6.Name := 'label6';
        self.label6.Size := new System.Drawing.Size(86, 24);
        self.label6.TabIndex := 9;
        self.label6.Text := 'Сортировка';
        self.label6.TextAlign := System.Drawing.ContentAlignment.MiddleRight;
        self.label6.Visible := false;
        self.label6.Click += label6_Click;
        // 
        // label7
        // 
        self.label7.Location := new System.Drawing.Point(22, 151);
        self.label7.Name := 'label7';
        self.label7.Size := new System.Drawing.Size(127, 24);
        self.label7.TabIndex := 10;
        self.label7.Text := 'Кол-во элементов';
        self.label7.TextAlign := System.Drawing.ContentAlignment.MiddleRight;
        self.label7.Visible := false;
        // 
        // label8
        // 
        self.label8.Location := new System.Drawing.Point(92, 181);
        self.label8.Name := 'label8';
        self.label8.Size := new System.Drawing.Size(57, 24);
        self.label8.TabIndex := 11;
        self.label8.Text := 'Случай';
        self.label8.TextAlign := System.Drawing.ContentAlignment.MiddleRight;
        self.label8.Visible := false;
        // 
        // button2
        // 
        self.button2.Font := new System.Drawing.Font('Microsoft Sans Serif', 16.2, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, (System.Byte(204)));
        self.button2.Location := new System.Drawing.Point(256, 234);
        self.button2.Name := 'button2';
        self.button2.Size := new System.Drawing.Size(192, 48);
        self.button2.TabIndex := 12;
        self.button2.Text := 'Начать';
        self.button2.UseVisualStyleBackColor := true;
        self.button2.Click += button2_Click;
        // 
        // label9
        // 
        self.label9.Font := new System.Drawing.Font('Microsoft Sans Serif', 16.2, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, (System.Byte(204)));
        self.label9.Location := new System.Drawing.Point(63, 116);
        self.label9.Name := 'label9';
        self.label9.Size := new System.Drawing.Size(564, 83);
        self.label9.TabIndex := 13;
        self.label9.Text := 'Эта программа создана на Pascal 3.8.1 для проверки сортировок.';
        self.label9.TextAlign := System.Drawing.ContentAlignment.MiddleCenter;
        // 
        // button3
        // 
        self.button3.Location := new System.Drawing.Point(155, 304);
        self.button3.Name := 'button3';
        self.button3.Size := new System.Drawing.Size(139, 40);
        self.button3.TabIndex := 14;
        self.button3.Text := 'Выйти из приложения';
        self.button3.UseVisualStyleBackColor := true;
        self.button3.Visible := false;
        self.button3.Click += button3_Click;
        // 
        // label10
        // 
        self.label10.Font := new System.Drawing.Font('Microsoft Sans Serif', 16.2, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, (System.Byte(204)));
        self.label10.Location := new System.Drawing.Point(63, 116);
        self.label10.Name := 'label10';
        self.label10.Size := new System.Drawing.Size(564, 83);
        self.label10.TabIndex := 15;
        self.label10.Text := 'Вы уверены, что хотите выйти?';
        self.label10.TextAlign := System.Drawing.ContentAlignment.MiddleCenter;
        self.label10.Visible := false;
        self.label10.Click += label10_Click;
        // 
        // button4
        // 
        self.button4.Font := new System.Drawing.Font('Microsoft Sans Serif', 16.2, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, (System.Byte(204)));
        self.button4.Location := new System.Drawing.Point(155, 234);
        self.button4.Name := 'button4';
        self.button4.Size := new System.Drawing.Size(192, 48);
        self.button4.TabIndex := 16;
        self.button4.Text := 'Нет';
        self.button4.UseVisualStyleBackColor := true;
        self.button4.Visible := false;
        self.button4.Click += button4_Click;
        // 
        // button5
        // 
        self.button5.Font := new System.Drawing.Font('Microsoft Sans Serif', 16.2, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, (System.Byte(204)));
        self.button5.Location := new System.Drawing.Point(384, 236);
        self.button5.Name := 'button5';
        self.button5.Size := new System.Drawing.Size(192, 48);
        self.button5.TabIndex := 17;
        self.button5.Text := 'Да';
        self.button5.UseVisualStyleBackColor := true;
        self.button5.Visible := false;
        self.button5.Click += button5_Click;
        // 
        // button6
        // 
        self.button6.Location := new System.Drawing.Point(155, 256);
        self.button6.Name := 'button6';
        self.button6.Size := new System.Drawing.Size(139, 42);
        self.button6.TabIndex := 18;
        self.button6.Text := 'Сгенерировать новые массивы';
        self.button6.UseVisualStyleBackColor := true;
        self.button6.Visible := false;
        self.button6.Click += button6_Click;
        // 
        // label11
        // 
        self.label11.Font := new System.Drawing.Font('Microsoft Sans Serif', 12, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, (System.Byte(204)));
        self.label11.Location := new System.Drawing.Point(373, 125);
        self.label11.Name := 'label11';
        self.label11.Size := new System.Drawing.Size(254, 84);
        self.label11.TabIndex := 19;
        self.label11.Text := 'Файл с массивами хранится в C:\PABCWork.NET\Temp';
        self.label11.TextAlign := System.Drawing.ContentAlignment.MiddleCenter;
        self.label11.Visible := false;
        self.label11.Click += label11_Click;
        // 
        // Form1
        // 
        self.ClientSize := new System.Drawing.Size(702, 433);
        self.Controls.Add(self.label11);
        self.Controls.Add(self.button6);
        self.Controls.Add(self.button5);
        self.Controls.Add(self.button4);
        self.Controls.Add(self.label10);
        self.Controls.Add(self.button3);
        self.Controls.Add(self.label9);
        self.Controls.Add(self.button2);
        self.Controls.Add(self.label8);
        self.Controls.Add(self.label7);
        self.Controls.Add(self.label6);
        self.Controls.Add(self.label5);
        self.Controls.Add(self.label4);
        self.Controls.Add(self.label3);
        self.Controls.Add(self.comboBox3);
        self.Controls.Add(self.label2);
        self.Controls.Add(self.label1);
        self.Controls.Add(self.button1);
        self.Controls.Add(self.comboBox2);
        self.Controls.Add(self.comboBox1);
        self.Name := 'Form1';
        self.Text := 'Check sort';
        self.ResumeLayout(false);
        self.PerformLayout();
    end;
